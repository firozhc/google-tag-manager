# google-tag-manager
Steps

Personal Access Token - 43ea15aa8a47834a7fdcb0a16538d747efa2abc9

1. Create GTM Account and Container
2. Enable GTM API from Google API Console
3. 

client id - 123054155439-5po5550bbaavikre8vog27ngtbmjgn7f.apps.googleusercontent.com
client secret - ZP4fluSDvTRyDcdAtc-TQjHo


1. get list of account for user and extract account ids - GET https://www.googleapis.com/tagmanager/v2/accounts 
2. {
3.  "account": [
4.   {
5.    "path": "accounts/1853485978",
6.    "accountId": "1853485978",
7.    "name": "Demo"
8.   },
9.   {
10.    "path": "accounts/1404042777",
11.    "accountId": "1404042777",
12.    "name": "TheMaverickAtWork"
13.   },
14.   {
15.    "path": "accounts/4521840438",
16.    "accountId": "4521840438",
17.    "name": "Test"
18.   }
19.  ]
20. }
21. 
22. 
23. call get container method using account id - 
24. GET https://www.googleapis.com/tagmanager/v2/+parent/containers
25. GET https://www.googleapis.com/tagmanager/v2/accounts/4521840438/containers
26. extract the relevant containers public id
27. {
28.  "container": [
29.   {
30.    "path": "accounts/4521840438/containers/10524766",
31.    "accountId": "4521840438",
32.    "containerId": "10524766",
33.    "name": "testcontainer",
34.    "publicId": "GTM-KB5S87G",
35.    "usageContext": [
36.     "web"
37.    ],
38.    "fingerprint": "1543440285059",
39.    "tagManagerUrl": "https://tagmanager.google.com/#/container/accounts/4521840438/containers/10524766/workspaces?apiLink=container"
40.   },
41.   {
42.    "path": "accounts/4521840438/containers/10525729",
43.    "accountId": "4521840438",
44.    "containerId": "10525729",
45.    "name": "Greetings",
46.    "publicId": "GTM-MXB9B22",
47.    "usageContext": [
48.     "web"
49.    ],
50.    "fingerprint": "1543474110180",
51.    "tagManagerUrl": "https://tagmanager.google.com/#/container/accounts/4521840438/containers/10525729/workspaces?apiLink=container"
52.   }
53.  ]
54. }
55. 
56. embed the relevant containers public id into page script
57. head tag
58. <!-- Google Tag Manager -->
59. <script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
60. new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
61. j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
62. 'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
63. })(window,document,'script','dataLayer','GTM-MXB9B22');</script>
64. <!-- End Google Tag Manager -->
65. 
66. body tag
67. <!-- Google Tag Manager (noscript) -->
68. <noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-MXB9B22"
69. height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
70. <!-- End Google Tag Manager (noscript) -->
