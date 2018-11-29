"""Access and manage a Google Tag Manager account."""

import argparse
import sys

import httplib2

from apiclient.discovery import build
from oauth2client import client
from oauth2client import file
from oauth2client import tools


def GetService(api_name, api_version, scope, client_secrets_path):
  """Get a service that communicates to a Google API.

  Args:
    api_name: string The name of the api to connect to.
    api_version: string The api version to connect to.
    scope: A list of strings representing the auth scopes to authorize for the
      connection.
    client_secrets_path: string A path to a valid client secrets file.

  Returns:
    A service that is connected to the specified API.
  """
  # Parse command-line arguments.
  parser = argparse.ArgumentParser(
      formatter_class=argparse.RawDescriptionHelpFormatter,
      parents=[tools.argparser])
  flags = parser.parse_args([])

  # Set up a Flow object to be used if we need to authenticate.
  flow = client.flow_from_clientsecrets(
      client_secrets_path, scope=scope,
      message=tools.message_if_missing(client_secrets_path))

  # Prepare credentials, and authorize HTTP object with them.
  # If the credentials don't exist or are invalid run through the native client
  # flow. The Storage object will ensure that if successful the good
  # credentials will get written back to a file.
  storage = file.Storage(api_name + '.dat')
  credentials = storage.get()
  if credentials is None or credentials.invalid:
    credentials = tools.run_flow(flow, storage, flags)
  http = credentials.authorize(http=httplib2.Http())

  # Build the service object.
  service = build(api_name, api_version, http=http)

  return service

def FindGreetingsContainer(service, account_path):
  """Find the greetings container.

  Args:
    service: the Tag Manager service object.
    account_path: the path of the Tag Manager account from which to retrieve the
      Greetings container.

  Returns:
    The greetings container if it exists, or None if it does not.
  """
  # Query the Tag Manager API to list all containers for the given account.
  container_wrapper = service.accounts().containers().list(
      parent=account_path).execute()

  # Find and return the Greetings container if it exists.
  for container in container_wrapper['container']:
    if container['name'] == 'Greetings':
      return container
  return None

def CreateWorkspace(service, container):
    """Creates a workspace named 'my workspace'.

    Args:
      service: the Tag Manager service object.
      container: the container to insert the workspace within.

    Returns:
      The created workspace.
    """
    return service.accounts().containers().workspaces().create(
        parent=container['path'],
        body={
            'name': 'my workspace',
        }).execute()

def CreateHelloWorldTag(service, workspace, tracking_id):
  """Create the Universal Analytics Hello World Tag.

  Args:
    service: the Tag Manager service object.
    workspace: the workspace to create a tag within.
    tracking_id: the Universal Analytics tracking ID to use.

  Returns:
    The created tag.
  """

  hello_world_tag = {
      'name': 'Universal Analytics Hello World',
      'type': 'ua',
      'parameter': [{
          'key': 'trackingId',
          'type': 'template',
          'value': str(tracking_id),
      }],
  }

  return service.accounts().containers().workspaces().tags().create(
      parent=workspace['path'],
      body=hello_world_tag).execute()


def CreateHelloWorldTrigger(service, workspace):
  """Create the Hello World Trigger.

  Args:
    service: the Tag Manager service object.
    workspace: the workspace to create the trigger within.

  Returns:
    The created trigger.
  """

  hello_world_trigger = {
      'name': 'Hello World Rule',
      'type': 'PAGEVIEW'
  }

  return service.accounts().containers().workspaces().triggers().create(
      parent=workspace['path'],
      body=hello_world_trigger).execute()

def UpdateHelloWorldTagWithTrigger(service, tag, trigger):
  """Update a Tag with a Trigger.

  Args:
    service: the Tag Manager service object.
    tag: the tag to associate with the trigger.
    trigger: the trigger to associate with the tag.
  """
  # Get the tag to update.
  tag = service.accounts().containers().workspaces().tags().get(
      path=tag['path']).execute()

  # Update the Firing Trigger for the Tag.
  tag['firingTriggerId'] = [trigger['triggerId']]

  # Update the Tag.
  response = service.accounts().containers().workspaces().tags().update(
      path=tag['path'],
      body=tag).execute()

def main(argv):
  # Get tag manager account ID from command line.
  assert len(argv) == 2 and 'usage: gtm-api-hello-world.py <account_id>'
  account_id = str(argv[1])
  account_path = 'accounts/%s' % account_id

  # Define the auth scopes to request.
  scope = ['https://www.googleapis.com/auth/tagmanager.edit.containers']

  # Authenticate and construct service.
  service = GetService('tagmanager', 'v2', scope, 'client_secrets.json')

  # Find the greetings container.
  container = FindGreetingsContainer(service, account_path)

  # Create a new workspace.
  workspace = CreateWorkspace(service, container)

  # Create the hello world tag.
  tag = CreateHelloWorldTag(
      service, workspace, 'UA-1234-5')

  # Create the hello world Trigger.
  trigger = CreateHelloWorldTrigger(
      service, workspace)

  # Update the hello world tag to fire based on the hello world tag.
  UpdateHelloWorldTagWithTrigger(service, tag, trigger)
  
if __name__ == '__main__':
  main(sys.argv)

    