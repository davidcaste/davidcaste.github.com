Title: Howto make Nginx decompress a gzipped request
Date: 2015-05-13
Modified: 2015-05-13
Category: sysadmin
Tags: nginx, lua, gzip

It is not usual, but sometimes it could be useful to receive compressed request bodies. Although clients and the service itself can benefit from lower bandwith usage, it is very dangerous because a small compressed file can be inflated to a relatively huge file. To handle such a request could exhaust the resources of the server, causing a [Denial of Service (DoS)](http://en.wikipedia.org/wiki/Denial-of-service_attack).

There are two options to handle compressed requests:

1. Let the backend service itself to decompress the request.
2. Use a proxy reverse server, like [Nginx](http://nginx.org/), handle the request and forward it to the backend service.

Both approximations have their own advantages or disadvantages, but ultimately it depends if the backend service is able to handle the compressed requests.

Apache provides a module called [mod_deflate](http://httpd.apache.org/docs/2.4/mod/mod_deflate.html) which can be used (among more things) to decompress gzipped requests. Unfortunately according to [this](http://forum.nginx.org/read.php?11,96472,214266) and [this](http://forum.nginx.org/read.php?2,246979,246994#msg-246994), Nginx doesn't seem to have that functionality right out of the box.

On the other hand, there is a Nginx module called [ngx_lua](http://wiki.nginx.org/HttpLuaModule), which according to its description:

>This module embeds Lua, via the standard Lua 5.1 interpreter or LuaJIT 2.0/2.1, into Nginx and by leveraging Nginx's subrequests, allows the integration of the powerful Lua threads (Lua coroutines) into the Nginx event model.

After spending a couple of days learning the basics of Lua and playing with Nginx, I wrote a Lua script to make Nginx handle requests with a gzipped body before handling the decompressed request to some backend server:

[gist:id=05b2f9461ebe4a3bb3fc]

Some things to take into consideration:

* The module `ngx_lua` is not included by default in Nginx. If you are using Debian or Ubuntu you must install package `nginx-extras` and its dependencies.
* A Lua module called [lzlib](https://github.com/LuaDist/lzlib) does the actual decompression of the requests body. Again, if you are using Debian or Ubuntu you must install package `lua-zib` and its dependencies.
* You really need to limit the maximum size of a request body and the maximum size of a decompressed/inflated body.
* A request handled by Nginx goes though a series of [phases](http://wiki.nginx.org/Phases). The request body must be manipulated before handling the request to the backend server, so the phase handler [rewrite_by_lua](http://wiki.nginx.org/HttpLuaModule#rewrite_by_lua) provided by `ngx_lua` is used.
* I've implemented some sanity checks to avoid some common misuse cases (e.g. corrupted body, not gzip-compressed, huge uncompressed body). In that case, Nginx does not forward the request to the backend server, and a `HTTP_BAD_REQUEST` status is returned instead.

Feel free to study, fork and use the gist above :-)