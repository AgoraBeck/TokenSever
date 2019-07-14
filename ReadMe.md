## Environment

1. python 2.7. 
2. postman

## How to use 

1.run python token server 

> python server.py 

2.getToken, 生产Token

![图1](https://github.com/AgoraBeck/TokenSever/blob/master/getToken.jpeg)


3.inverseToken
 
 ![图2](https://github.com/AgoraBeck/TokenSever/blob/master/inverseToken.jpeg)

4.Android client json http request 

```
 //Change YOUR_SERVER_IP
 static final String DYNAMIC_KEY_SERVICE_URL_PREFIX = "http://<YOUR_SERVER_IP>:8081";

    private String readStream(InputStream in) {
        BufferedReader reader = null;
        StringBuffer response = new StringBuffer();
        try {
            reader = new BufferedReader(new InputStreamReader(in));
            String line = "";
            while ((line = reader.readLine()) != null) {
                response.append(line);
            }
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            if (reader != null) {
                try {
                    reader.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }
        return response.toString();
    }

    private String sendPost(String pUrl, String param){
        String responseString = "";
        try {
            URL url = new URL(pUrl);
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();
            connection.setConnectTimeout(5000);
            connection.setRequestMethod("POST");
            connection.setRequestProperty("Content-Type","application/json; charset=UTF-8");
            connection.setRequestProperty("Accept", "application/json");
            connection.setDoOutput(true);

            OutputStream out = connection.getOutputStream();
            out.write(param.getBytes("utf-8"),0, param.length());
            out.flush();
            out.close();

            // try to get response
            int responseCode = connection.getResponseCode();
            if(responseCode ==200){
                //请求成功
                responseString = readStream(connection.getInputStream());
                Log.v("CatalogClient-Response", responseString);
            }
        } catch (MalformedURLException e) {
            e.printStackTrace();
        } catch (ProtocolException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }

        // Parse Json returned.
        String token = "";
        try {
            JSONObject jObj = new JSONObject(responseString);
            token = jObj.getString("token");
            Log.v("totalItems",token);

        } catch (JSONException e) {
            Log.e("CatalogClient", "unexpected JSON exception", e);
        }
        return token;
    }

    String getToken(String cname, int uid){
        JSONObject jsondata = new JSONObject();
        try {
            jsondata.put("cname", cname);
        } catch (Exception e ) {

        }
        try {
            jsondata.put("uid", uid);
        } catch (Exception e) {

        }

        //send post json data
        String s1 = sendPost(DYNAMIC_KEY_SERVICE_URL_PREFIX + "/getToken", jsondata.toString());
        Log.i(LOG_TAG, "token: " + s1);
        return s1;
    }

	//Get token
   new Thread(new Runnable(){
        @Override
        public void run() {
        	getToken("beck", 1);
        }
    }).start();


```

Ref: 

> 1.![Making a JSON POST Request With HttpURLConnection](https://www.baeldung.com/httpurlconnection-post)

> 2.![Make HTTP request and parse JSON data from Android by using HttpURLConnection](https://gist.github.com/hnaoto/f492c9ceae264897dd6f)
