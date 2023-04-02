ASUS RT-AX92U sql injection

Firmware version - 3.0.0.4.386_45934

When AiCloud 2.0 Cloud Disk functionality is enabled, the router start lighttpd server on port 443.

There is a sql injection bug when parsing PROPFINDMEDIALIST HTTP request.

Consider the following code from mod_webdav.c:

```
 case HTTP_METHOD_PROPFINDMEDIALIST:{

	 			if (NULL != (ds = (data_string *)array_get_element(con->request.headers, "Keyword"))) {
                        keyword = ds->value;
                }

				...
[1]                if (!buffer_is_empty(keyword) && 
                    (strstr(keyword->ptr, "'")!=NULL ||
                        keyword->used > 200)) {

                        Cdbg(DBE, "The paramter keyword is invalid!");
                        con->http_status = 207;
                        con->file_finished = 1;
                        return HANDLER_FINISHED;
                }
				...
				if(!buffer_is_empty(keyword)){                  
[2]                        buffer_urldecode_path(keyword);

                        if(strstr(keyword->ptr, "*")||strstr(keyword->ptr, "?")){
                                char buff[200];
                                replace_str(keyword->ptr, "*", "%", buff);
                                replace_str(buff, "?", "_", buff);
                                sprintf(sql_query, "%s and ( PATH LIKE '%s' or TITLE LIKE '%s' )", sql_query, buff, buff);
                        }
                        else
                                sprintf(sql_query, "%s and ( PATH LIKE '%s%s%s' or TITLE LIKE '%s%s%s' )", sql_query, "%", keyword->ptr, "%", "%", keyword->ptr, "%");
                }
		...
}

Check on line #1 is not enough as 'keyword' variable is decoded on line #2 before calling sprintf.
```

How to verify:
```
1) insert usb media
2) enable Cloud Disk (AiCloud 2.0 -> Cloud Disk)
3) run t1.py
4) file /tmp/hello.db should be created on a router
# ls -al /tmp/hello.db 
-rw-r--r--    1 admin    root          8192 Nov 21 13:12 /tmp/hello.db
```

