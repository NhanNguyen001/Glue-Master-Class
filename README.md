message
"exception"

exception.message
"Read timed out"

exception.type
"java.net.SocketTimeoutException"

exception.stacktrace
"java.net.SocketTimeoutException: Read timed out
at java.base/sun.nio.ch.NioSocketImpl.timedRead(NioSocketImpl.java:283)
at java.base/sun.nio.ch.NioSocketImpl.implRead(NioSocketImpl.java:309)
at java.base/sun.nio.ch.NioSocketImpl.read(NioSocketImpl.java:350)
at java.base/sun.nio.ch.NioSocketImpl$1.read(NioSocketImpl.java:803)
	at java.base/java.net.Socket$SocketInputStream.read(Socket.java:966)
at java.base/sun.security.ssl.SSLSocketInputRecord.read(SSLSocketInputRecord.java:478)
at java.base/sun.security.ssl.SSLSocketInputRecord.readHeader(SSLSocketInputRecord.java:472)
at java.base/sun.security.ssl.SSLSocketInputRecord.bytesInCompletePacket(SSLSocketInputRecord.java:70)
at java.base/sun.security.ssl.SSLSocketImpl.readApplicationRecord(SSLSocketImpl.java:1460)
at java.base/sun.security.ssl.SSLSocketImpl$AppInputStream.read(SSLSocketImpl.java:1064)
	at java.base/java.io.BufferedInputStream.fill(BufferedInputStream.java:244)
	at java.base/java.io.BufferedInputStream.read1(BufferedInputStream.java:284)
	at java.base/java.io.BufferedInputStream.read(BufferedInputStream.java:343)
	at java.base/sun.net.www.http.HttpClient.parseHTTPHeader(HttpClient.java:824)
	at java.base/sun.net.www.http.HttpClient.parseHTTP(HttpClient.java:759)
	at java.base/sun.net.www.protocol.http.HttpURLConnection.getInputStream0(HttpURLConnection.java:1688)
	at java.base/sun.net.www.protocol.http.HttpURLConnection.getInputStream(HttpURLConnection.java:1589)
	at java.base/java.net.HttpURLConnection.getResponseCode(HttpURLConnection.java:529)
	at java.base/sun.net.www.protocol.https.HttpsURLConnectionImpl.getResponseCode(HttpsURLConnectionImpl.java:308)
	at feign.Client$Default.convertResponse(Client.java:110)
at feign.Client$Default.execute(Client.java:106)
	at feign.SynchronousMethodHandler.executeAndDecode(SynchronousMethodHandler.java:102)
	at feign.SynchronousMethodHandler.invoke(SynchronousMethodHandler.java:72)
	at feign.ReflectiveFeign$FeignInvocationHandler.invoke(ReflectiveFeign.java:98)
at jdk.proxy3/jdk.proxy3.$Proxy225.getSavingAccountInfoByClientNo(Unknown Source)
	at com.hdbank.deposit.infra.service.TDAccountServiceImpl.getSavingAccountInfoByClientNo(TDAccountServiceImpl.java:386)
	at jdk.internal.reflect.GeneratedMethodAccessor298.invoke(Unknown Source)
	at java.base/jdk.internal.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)
	at java.base/java.lang.reflect.Method.invoke(Method.java:568)
	at org.springframework.aop.support.AopUtils.invokeJoinpointUsingReflection(AopUtils.java:343)
	at org.springframework.aop.framework.JdkDynamicAopProxy.invoke(JdkDynamicAopProxy.java:211)
	at jdk.proxy3/jdk.proxy3.$Proxy243.getSavingAccountInfoByClientNo(Unknown Source)
at com.hdbank.deposit.infra.service.CasaAccountServiceImpl.lambda$getAccountInfoByClientNo$1(CasaAccountServiceImpl.java:133)
	at java.base/java.util.concurrent.CompletableFuture$AsyncSupply.run(CompletableFuture.java:1768)
at java.base/java.lang.Thread.run(Thread.java:833)
"
