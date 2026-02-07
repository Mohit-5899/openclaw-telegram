 telegram-clawdbot git:(main) ✗ docker compose up
[+] Building 80.7s (15/15) FINISHED                                                                                              
 => [internal] load local bake definitions                                                                                  0.0s
 => => reading from stdin 449B                                                                                              0.0s
 => [internal] load build definition from Dockerfile                                                                        0.0s
 => => transferring dockerfile: 674B                                                                                        0.0s
 => [internal] load metadata for docker.io/library/python:3.12-slim                                                         5.5s
 => [internal] load .dockerignore                                                                                           0.0s
 => => transferring context: 186B                                                                                           0.0s
 => [1/8] FROM docker.io/library/python:3.12-slim@sha256:9e01bf1ae5db7649a236da7be1e94ffbbbdd7a93f867dd0d8d5720d9e1f89fab   4.1s
 => => resolve docker.io/library/python:3.12-slim@sha256:9e01bf1ae5db7649a236da7be1e94ffbbbdd7a93f867dd0d8d5720d9e1f89fab   0.0s
 => => sha256:09fa645f2e8f01bf76e8432e1b0c11b79a8726f64b60501af160c71b7c3917ab 251B / 251B                                  1.8s
 => => sha256:acb1cdc2efd2dd71f63d83424a85f331eff1c0414904ac281b16fb476566c578 12.04MB / 12.04MB                            3.9s
 => => sha256:bfa636a0362e220d4ce65597cd26d0ae68f82e42769c36d28feb1c96d1214c12 1.27MB / 1.27MB                              2.0s
 => => extracting sha256:bfa636a0362e220d4ce65597cd26d0ae68f82e42769c36d28feb1c96d1214c12                                   0.0s
 => => extracting sha256:acb1cdc2efd2dd71f63d83424a85f331eff1c0414904ac281b16fb476566c578                                   0.1s
 => => extracting sha256:09fa645f2e8f01bf76e8432e1b0c11b79a8726f64b60501af160c71b7c3917ab                                   0.0s
 => [internal] load build context                                                                                           0.1s
 => => transferring context: 113.14kB                                                                                       0.0s
 => [2/8] RUN apt-get update &&     apt-get install -y --no-install-recommends curl &&     curl -fsSL https://deb.nodesou  35.1s
 => [3/8] WORKDIR /app                                                                                                      0.0s 
 => [4/8] COPY requirements.txt .                                                                                           0.0s 
 => [5/8] RUN pip install --no-cache-dir -r requirements.txt                                                               30.0s 
 => [6/8] COPY src/ src/                                                                                                    0.0s 
 => [7/8] COPY mcp-config.json .                                                                                            0.0s 
 => [8/8] RUN mkdir -p data logs                                                                                            0.1s 
 => exporting to image                                                                                                      5.4s
 => => exporting layers                                                                                                     4.1s
 => => exporting manifest sha256:f663fdddb08c0df5a3c0f98fc2013b6ecff359adf992a712e4930e5a88219a33                           0.0s
 => => exporting config sha256:81f7a0ed4388322417c506f3e0531be43f8aee05afbe0f0d2f7f8869744224e9                             0.0s
 => => exporting attestation manifest sha256:4cc7328f1c13e32d039045c0347bbe0067b3b3bfd06ec26bcae1357ed804278f               0.0s
 => => exporting manifest list sha256:8a6c3ef9d0121233757bd09b19894a6f07508d48b8d455ddc765ea9af4981ea8                      0.0s
 => => naming to docker.io/library/telegram-clawdbot-clawdbot:latest                                                        0.0s
 => => unpacking to docker.io/library/telegram-clawdbot-clawdbot:latest                                                     1.3s
 => resolving provenance for metadata file                                                                                  0.0s
[+] Running 5/5
 ✔ clawdbot                                  Built                                                                          0.0s 
 ✔ Network telegram-clawdbot_default         Created                                                                        0.0s 
 ✔ Volume "telegram-clawdbot_clawdbot-data"  Created                                                                        0.0s 
 ✔ Volume "telegram-clawdbot_clawdbot-logs"  Created                                                                        0.0s 
 ✔ Container clawdbot                        Created                                                                        0.4s 
Attaching to clawdbot
clawdbot  | ==================================================
clawdbot  | Starting Telegram ClawdBot
clawdbot  | ==================================================
clawdbot  | 2026-02-07 15:32:13 [INFO] main: Configuration loaded
clawdbot  | 2026-02-07 15:32:13 [INFO] main: Initializing database...
clawdbot  | 2026-02-07 15:32:13 [INFO] database: Initializing database at data/clawdbot.db
clawdbot  | 2026-02-07 15:32:13 [INFO] database: Database initialized successfully
clawdbot  | 2026-02-07 15:32:13 [INFO] main: Initializing RAG system...
clawdbot  | 2026-02-07 15:32:13 [INFO] vectorstore: Vector store initialized
clawdbot  | 2026-02-07 15:32:13 [INFO] indexer: Indexer started (indexes on-demand via index_single_message)
clawdbot  | 2026-02-07 15:32:13 [INFO] main: Initializing Memory system...
clawdbot  | 2026-02-07 15:32:13 [INFO] mem0-client: Initializing mem0 cloud client...
clawdbot  | 2026-02-07 15:32:16 [INFO] httpx: HTTP Request: GET https://api.mem0.ai/v1/ping/ "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:32:16 [INFO] mem0-client: ✅ mem0 cloud client initialized
clawdbot  | 2026-02-07 15:32:16 [INFO] main: Initializing MCP servers...
clawdbot  | 2026-02-07 15:32:16 [INFO] mcp-client: Initializing MCP servers...
clawdbot  | 2026-02-07 15:32:16 [INFO] mcp-config: Loaded 2 MCP servers from config file
clawdbot  | 2026-02-07 15:32:16 [INFO] mcp-client: Connecting to MCP server: github
clawdbot  | 2026-02-07 15:32:24 [INFO] mcp-client: Server github connected with 26 tools
clawdbot  | 2026-02-07 15:32:24 [INFO] mcp-client: Connecting to MCP server: notion
clawdbot  | 2026-02-07 15:32:37 [INFO] mcp-client: Server notion connected with 22 tools
clawdbot  | 2026-02-07 15:32:37 [INFO] mcp-client: MCP initialized: 2 servers, 48 tools
clawdbot  | 2026-02-07 15:32:37 [INFO] main: Starting task scheduler...
clawdbot  | 2026-02-07 15:32:37 [INFO] apscheduler.scheduler: Scheduler started
clawdbot  | 2026-02-07 15:32:37 [INFO] scheduler: Task scheduler started
clawdbot  | 2026-02-07 15:32:37 [INFO] apscheduler.scheduler: Added job "TaskScheduler._check_pending_tasks" to job store "default"
clawdbot  | 2026-02-07 15:32:37 [INFO] main: Creating Telegram bot...
clawdbot  | 2026-02-07 15:32:37 [INFO] telegram-bot: Creating Telegram application...
clawdbot  | 2026-02-07 15:32:37 [INFO] handlers: Handlers registered
clawdbot  | 2026-02-07 15:32:37 [INFO] telegram-bot: Telegram application created
clawdbot  | 2026-02-07 15:32:37 [INFO] main: ==================================================
clawdbot  | 2026-02-07 15:32:37 [INFO] main: 🚀 Telegram ClawdBot is running!
clawdbot  | 2026-02-07 15:32:37 [INFO] main: ==================================================
clawdbot  | 2026-02-07 15:32:37 [INFO] main:   Model: claude-opus-4-6
clawdbot  | 2026-02-07 15:32:37 [INFO] main:   RAG: ✅ Enabled
clawdbot  | 2026-02-07 15:32:37 [INFO] main:   Memory: ✅ Enabled
clawdbot  | 2026-02-07 15:32:37 [INFO] main:   GitHub MCP: ✅
clawdbot  | 2026-02-07 15:32:37 [INFO] main:   Notion MCP: ✅
clawdbot  | 2026-02-07 15:32:37 [INFO] main: ==================================================
clawdbot  | 2026-02-07 15:32:41 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getMe "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:32:41 [INFO] apscheduler.scheduler: Scheduler started
clawdbot  | 2026-02-07 15:32:41 [INFO] telegram.ext.Application: Application started
clawdbot  | 2026-02-07 15:32:41 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/deleteWebhook "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:32:52 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:33:03 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:33:04 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:33:05 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/sendMessage "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:33:14 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:33:24 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:33:32 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:33:32 [INFO] handlers: Message from MOHIT (980731551): Hi...
clawdbot  | 2026-02-07 15:33:34 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/sendChatAction "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:33:35 [INFO] httpx: HTTP Request: POST https://api.mem0.ai/v2/memories/search/ "HTTP/1.1 400 Bad Request"
clawdbot  | 2026-02-07 15:33:35 [ERROR] mem0.client.utils: HTTP error occurred: Client error '400 Bad Request' for url 'https://api.mem0.ai/v2/memories/search/'
clawdbot  | For more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/400
clawdbot  | 2026-02-07 15:33:35 [ERROR] mem0-client: Failed to search memory: {"error":"Filters are required and cannot be empty. Please refer to https://docs.mem0.ai/api-reference/memory/search-memories"}
clawdbot  | 2026-02-07 15:33:35 [INFO] agent: Calling Claude with 60 tools
clawdbot  | 2026-02-07 15:33:40 [INFO] httpx: HTTP Request: POST https://api.anthropic.com/v1/messages "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:33:41 [INFO] httpx: HTTP Request: POST https://api.mem0.ai/v1/memories/ "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:33:41 [INFO] mem0-client: Stored 1 memories for user 980731551
clawdbot  | 2026-02-07 15:33:41 [WARNING] apscheduler.executors.default: Run time of job "TaskScheduler._check_pending_tasks (trigger: interval[0:01:00], next run at: 2026-02-07 15:34:37 UTC)" was missed by 0:00:04.216237
clawdbot  | 2026-02-07 15:33:42 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/sendMessage "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:33:43 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:33:53 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:34:03 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:34:14 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:34:24 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:34:34 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:34:37 [INFO] apscheduler.executors.default: Running job "TaskScheduler._check_pending_tasks (trigger: interval[0:01:00], next run at: 2026-02-07 15:35:37 UTC)" (scheduled at 2026-02-07 15:34:37.055516+00:00)
clawdbot  | 2026-02-07 15:34:37 [INFO] apscheduler.executors.default: Job "TaskScheduler._check_pending_tasks (trigger: interval[0:01:00], next run at: 2026-02-07 15:35:37 UTC)" executed successfully
clawdbot  | 2026-02-07 15:34:45 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:34:55 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:35:05 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:35:16 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:35:26 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:35:37 [INFO] apscheduler.executors.default: Running job "TaskScheduler._check_pending_tasks (trigger: interval[0:01:00], next run at: 2026-02-07 15:36:37 UTC)" (scheduled at 2026-02-07 15:35:37.055516+00:00)
clawdbot  | 2026-02-07 15:35:37 [INFO] apscheduler.executors.default: Job "TaskScheduler._check_pending_tasks (trigger: interval[0:01:00], next run at: 2026-02-07 15:36:37 UTC)" executed successfully
clawdbot  | 2026-02-07 15:35:41 [ERROR] telegram.ext.Updater: Exception happened while polling for updates.
clawdbot  | Traceback (most recent call last):
clawdbot  |   File "/usr/local/lib/python3.12/site-packages/httpx/_transports/default.py", line 101, in map_httpcore_exceptions
clawdbot  |     yield
clawdbot  |   File "/usr/local/lib/python3.12/site-packages/httpx/_transports/default.py", line 394, in handle_async_request
clawdbot  |     resp = await self._pool.handle_async_request(req)
clawdbot  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
clawdbot  |   File "/usr/local/lib/python3.12/site-packages/httpcore/_async/connection_pool.py", line 256, in handle_async_request
clawdbot  |     raise exc from None
clawdbot  |   File "/usr/local/lib/python3.12/site-packages/httpcore/_async/connection_pool.py", line 236, in handle_async_request
clawdbot  |     response = await connection.handle_async_request(
clawdbot  |                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
clawdbot  |   File "/usr/local/lib/python3.12/site-packages/httpcore/_async/connection.py", line 103, in handle_async_request
clawdbot  |     return await self._connection.handle_async_request(request)
clawdbot  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
clawdbot  |   File "/usr/local/lib/python3.12/site-packages/httpcore/_async/http11.py", line 136, in handle_async_request
clawdbot  |     raise exc
clawdbot  |   File "/usr/local/lib/python3.12/site-packages/httpcore/_async/http11.py", line 106, in handle_async_request
clawdbot  |     ) = await self._receive_response_headers(**kwargs)
clawdbot  |         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
clawdbot  |   File "/usr/local/lib/python3.12/site-packages/httpcore/_async/http11.py", line 177, in _receive_response_headers
clawdbot  |     event = await self._receive_event(timeout=timeout)
clawdbot  |             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
clawdbot  |   File "/usr/local/lib/python3.12/site-packages/httpcore/_async/http11.py", line 231, in _receive_event
clawdbot  |     raise RemoteProtocolError(msg)
clawdbot  | httpcore.RemoteProtocolError: Server disconnected without sending a response.
clawdbot  | 
clawdbot  | The above exception was the direct cause of the following exception:
clawdbot  | 
clawdbot  | Traceback (most recent call last):
clawdbot  |   File "/usr/local/lib/python3.12/site-packages/telegram/request/_httpxrequest.py", line 279, in do_request
clawdbot  |     res = await self._client.request(
clawdbot  |           ^^^^^^^^^^^^^^^^^^^^^^^^^^^
clawdbot  |   File "/usr/local/lib/python3.12/site-packages/httpx/_client.py", line 1540, in request
clawdbot  |     return await self.send(request, auth=auth, follow_redirects=follow_redirects)
clawdbot  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
clawdbot  |   File "/usr/local/lib/python3.12/site-packages/httpx/_client.py", line 1629, in send
clawdbot  |     response = await self._send_handling_auth(
clawdbot  |                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
clawdbot  |   File "/usr/local/lib/python3.12/site-packages/httpx/_client.py", line 1657, in _send_handling_auth
clawdbot  |     response = await self._send_handling_redirects(
clawdbot  |                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
clawdbot  |   File "/usr/local/lib/python3.12/site-packages/httpx/_client.py", line 1694, in _send_handling_redirects
clawdbot  |     response = await self._send_single_request(request)
clawdbot  |                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
clawdbot  |   File "/usr/local/lib/python3.12/site-packages/httpx/_client.py", line 1730, in _send_single_request
clawdbot  |     response = await transport.handle_async_request(request)
clawdbot  |                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
clawdbot  |   File "/usr/local/lib/python3.12/site-packages/httpx/_transports/default.py", line 393, in handle_async_request
clawdbot  |     with map_httpcore_exceptions():
clawdbot  |          ^^^^^^^^^^^^^^^^^^^^^^^^^
clawdbot  |   File "/usr/local/lib/python3.12/contextlib.py", line 158, in __exit__
clawdbot  |     self.gen.throw(value)
clawdbot  |   File "/usr/local/lib/python3.12/site-packages/httpx/_transports/default.py", line 118, in map_httpcore_exceptions
clawdbot  |     raise mapped_exc(message) from exc
clawdbot  | httpx.RemoteProtocolError: Server disconnected without sending a response.
clawdbot  | 
clawdbot  | The above exception was the direct cause of the following exception:
clawdbot  | 
clawdbot  | Traceback (most recent call last):
clawdbot  |   File "/usr/local/lib/python3.12/site-packages/telegram/ext/_utils/networkloop.py", line 161, in network_retry_loop
clawdbot  |     await do_action()
clawdbot  |   File "/usr/local/lib/python3.12/site-packages/telegram/ext/_utils/networkloop.py", line 154, in do_action
clawdbot  |     action_cb_task.result()
clawdbot  |   File "/usr/local/lib/python3.12/site-packages/telegram/ext/_updater.py", line 340, in polling_action_cb
clawdbot  |     updates = await self.bot.get_updates(
clawdbot  |               ^^^^^^^^^^^^^^^^^^^^^^^^^^^
clawdbot  |   File "/usr/local/lib/python3.12/site-packages/telegram/ext/_extbot.py", line 671, in get_updates
clawdbot  |     updates = await super().get_updates(
clawdbot  |               ^^^^^^^^^^^^^^^^^^^^^^^^^^
clawdbot  |   File "/usr/local/lib/python3.12/site-packages/telegram/_bot.py", line 4860, in get_updates
clawdbot  |     await self._post(
clawdbot  |   File "/usr/local/lib/python3.12/site-packages/telegram/_bot.py", line 703, in _post
clawdbot  |     return await self._do_post(
clawdbot  |            ^^^^^^^^^^^^^^^^^^^^
clawdbot  |   File "/usr/local/lib/python3.12/site-packages/telegram/ext/_extbot.py", line 369, in _do_post
clawdbot  |     return await super()._do_post(
clawdbot  |            ^^^^^^^^^^^^^^^^^^^^^^^
clawdbot  |   File "/usr/local/lib/python3.12/site-packages/telegram/_bot.py", line 732, in _do_post
clawdbot  |     result = await request.post(
clawdbot  |              ^^^^^^^^^^^^^^^^^^^
clawdbot  |   File "/usr/local/lib/python3.12/site-packages/telegram/request/_baserequest.py", line 198, in post
clawdbot  |     result = await self._request_wrapper(
clawdbot  |              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
clawdbot  |   File "/usr/local/lib/python3.12/site-packages/telegram/request/_baserequest.py", line 305, in _request_wrapper
clawdbot  |     code, payload = await self.do_request(
clawdbot  |                     ^^^^^^^^^^^^^^^^^^^^^^
clawdbot  |   File "/usr/local/lib/python3.12/site-packages/telegram/request/_httpxrequest.py", line 303, in do_request
clawdbot  |     raise NetworkError(f"httpx.{err.__class__.__name__}: {err}") from err
clawdbot  | telegram.error.NetworkError: httpx.RemoteProtocolError: Server disconnected without sending a response.
clawdbot  | 2026-02-07 15:35:52 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:36:03 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:36:13 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:36:23 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:36:34 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:36:37 [INFO] apscheduler.executors.default: Running job "TaskScheduler._check_pending_tasks (trigger: interval[0:01:00], next run at: 2026-02-07 15:37:37 UTC)" (scheduled at 2026-02-07 15:36:37.055516+00:00)
clawdbot  | 2026-02-07 15:36:37 [INFO] apscheduler.executors.default: Job "TaskScheduler._check_pending_tasks (trigger: interval[0:01:00], next run at: 2026-02-07 15:37:37 UTC)" executed successfully
clawdbot  | 2026-02-07 15:36:44 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:36:55 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:37:05 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:37:15 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:37:25 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:37:36 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:37:37 [INFO] apscheduler.executors.default: Running job "TaskScheduler._check_pending_tasks (trigger: interval[0:01:00], next run at: 2026-02-07 15:38:37 UTC)" (scheduled at 2026-02-07 15:37:37.055516+00:00)
clawdbot  | 2026-02-07 15:37:37 [INFO] apscheduler.executors.default: Job "TaskScheduler._check_pending_tasks (trigger: interval[0:01:00], next run at: 2026-02-07 15:38:37 UTC)" executed successfully
clawdbot  | 2026-02-07 15:38:06 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:38:16 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:38:27 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:38:37 [INFO] apscheduler.executors.default: Running job "TaskScheduler._check_pending_tasks (trigger: interval[0:01:00], next run at: 2026-02-07 15:39:37 UTC)" (scheduled at 2026-02-07 15:38:37.055516+00:00)
clawdbot  | 2026-02-07 15:38:37 [INFO] apscheduler.executors.default: Job "TaskScheduler._check_pending_tasks (trigger: interval[0:01:00], next run at: 2026-02-07 15:39:37 UTC)" executed successfully
clawdbot  | 2026-02-07 15:38:40 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:38:51 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:39:01 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:39:12 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:39:22 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:39:32 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:39:37 [INFO] apscheduler.executors.default: Running job "TaskScheduler._check_pending_tasks (trigger: interval[0:01:00], next run at: 2026-02-07 15:40:37 UTC)" (scheduled at 2026-02-07 15:39:37.055516+00:00)
clawdbot  | 2026-02-07 15:39:37 [INFO] apscheduler.executors.default: Job "TaskScheduler._check_pending_tasks (trigger: interval[0:01:00], next run at: 2026-02-07 15:40:37 UTC)" executed successfully
clawdbot  | 2026-02-07 15:39:43 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:39:54 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:40:05 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:40:13 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:40:13 [INFO] handlers: Message from MOHIT (980731551): what can you do for notion for me...
clawdbot  | 2026-02-07 15:40:17 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/sendChatAction "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:40:24 [INFO] httpx: HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:40:24 [INFO] vectorstore: Added 1 documents to vector store
clawdbot  | 2026-02-07 15:40:26 [INFO] httpx: HTTP Request: POST https://api.mem0.ai/v2/memories/search/ "HTTP/1.1 400 Bad Request"
clawdbot  | 2026-02-07 15:40:26 [ERROR] mem0.client.utils: HTTP error occurred: Client error '400 Bad Request' for url 'https://api.mem0.ai/v2/memories/search/'
clawdbot  | For more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/400
clawdbot  | 2026-02-07 15:40:26 [ERROR] mem0-client: Failed to search memory: {"error":"Filters are required and cannot be empty. Please refer to https://docs.mem0.ai/api-reference/memory/search-memories"}
clawdbot  | 2026-02-07 15:40:26 [INFO] retriever: Retrieving for query: "what can you do for notion for me..."
clawdbot  | 2026-02-07 15:40:28 [INFO] httpx: HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:40:28 [INFO] retriever: Retrieved 1 documents in 1906ms
clawdbot  | 2026-02-07 15:40:28 [INFO] agent: Retrieved 1 RAG results
clawdbot  | 2026-02-07 15:40:28 [INFO] agent: Calling Claude with 60 tools
clawdbot  | 2026-02-07 15:40:40 [INFO] httpx: HTTP Request: POST https://api.anthropic.com/v1/messages "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:40:43 [INFO] httpx: HTTP Request: POST https://api.mem0.ai/v1/memories/ "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:40:43 [INFO] mem0-client: Stored 1 memories for user 980731551
clawdbot  | 2026-02-07 15:40:43 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:40:43 [WARNING] apscheduler.executors.default: Run time of job "TaskScheduler._check_pending_tasks (trigger: interval[0:01:00], next run at: 2026-02-07 15:41:37 UTC)" was missed by 0:00:05.985679
clawdbot  | 2026-02-07 15:40:46 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/sendMessage "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:40:55 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:41:06 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:41:17 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:41:20 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:41:20 [INFO] handlers: Message from MOHIT (980731551): can you give me list of pages...
clawdbot  | 2026-02-07 15:41:23 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/sendChatAction "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:41:25 [INFO] httpx: HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:41:25 [INFO] vectorstore: Added 1 documents to vector store
clawdbot  | 2026-02-07 15:41:27 [INFO] httpx: HTTP Request: POST https://api.mem0.ai/v2/memories/search/ "HTTP/1.1 400 Bad Request"
clawdbot  | 2026-02-07 15:41:27 [ERROR] mem0.client.utils: HTTP error occurred: Client error '400 Bad Request' for url 'https://api.mem0.ai/v2/memories/search/'
clawdbot  | For more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/400
clawdbot  | 2026-02-07 15:41:27 [ERROR] mem0-client: Failed to search memory: {"error":"Filters are required and cannot be empty. Please refer to https://docs.mem0.ai/api-reference/memory/search-memories"}
clawdbot  | 2026-02-07 15:41:27 [INFO] agent: Calling Claude with 60 tools
clawdbot  | 2026-02-07 15:41:34 [INFO] httpx: HTTP Request: POST https://api.anthropic.com/v1/messages "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:41:34 [INFO] agent: Tool call: notion_API-post-search({'filter': {'property': 'object', 'value': 'page'}})
clawdbot  | 2026-02-07 15:41:34 [INFO] agent: Executing tool: notion_API-post-search
clawdbot  | 2026-02-07 15:41:34 [INFO] mcp-client: Executing MCP tool: notion/API-post-search
clawdbot  | 2026-02-07 15:41:34 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:41:37 [INFO] apscheduler.executors.default: Running job "TaskScheduler._check_pending_tasks (trigger: interval[0:01:00], next run at: 2026-02-07 15:42:37 UTC)" (scheduled at 2026-02-07 15:41:37.055516+00:00)
clawdbot  | 2026-02-07 15:41:37 [INFO] apscheduler.executors.default: Job "TaskScheduler._check_pending_tasks (trigger: interval[0:01:00], next run at: 2026-02-07 15:42:37 UTC)" executed successfully
clawdbot  | 2026-02-07 15:41:44 [INFO] httpx: HTTP Request: POST https://api.anthropic.com/v1/messages "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:41:47 [INFO] httpx: HTTP Request: POST https://api.mem0.ai/v1/memories/ "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:41:47 [INFO] mem0-client: Stored 1 memories for user 980731551
clawdbot  | 2026-02-07 15:41:47 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:41:51 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/sendMessage "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:41:58 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:42:09 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:42:19 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:42:30 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:42:37 [INFO] apscheduler.executors.default: Running job "TaskScheduler._check_pending_tasks (trigger: interval[0:01:00], next run at: 2026-02-07 15:43:37 UTC)" (scheduled at 2026-02-07 15:42:37.055516+00:00)
clawdbot  | 2026-02-07 15:42:37 [INFO] apscheduler.executors.default: Job "TaskScheduler._check_pending_tasks (trigger: interval[0:01:00], next run at: 2026-02-07 15:43:37 UTC)" executed successfully
clawdbot  | 2026-02-07 15:42:40 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:42:42 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:42:42 [INFO] handlers: Message from MOHIT (980731551): what you can do for my github...
clawdbot  | 2026-02-07 15:42:47 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/sendChatAction "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:42:51 [INFO] httpx: HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:42:51 [INFO] vectorstore: Added 1 documents to vector store
clawdbot  | 2026-02-07 15:42:53 [INFO] httpx: HTTP Request: POST https://api.mem0.ai/v2/memories/search/ "HTTP/1.1 400 Bad Request"
clawdbot  | 2026-02-07 15:42:53 [ERROR] mem0.client.utils: HTTP error occurred: Client error '400 Bad Request' for url 'https://api.mem0.ai/v2/memories/search/'
clawdbot  | For more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/400
clawdbot  | 2026-02-07 15:42:53 [ERROR] mem0-client: Failed to search memory: {"error":"Filters are required and cannot be empty. Please refer to https://docs.mem0.ai/api-reference/memory/search-memories"}
clawdbot  | 2026-02-07 15:42:53 [INFO] retriever: Retrieving for query: "what you can do for my github..."
clawdbot  | 2026-02-07 15:42:55 [INFO] httpx: HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:42:55 [INFO] retriever: Retrieved 3 documents in 1496ms
clawdbot  | 2026-02-07 15:42:55 [INFO] agent: Retrieved 3 RAG results
clawdbot  | 2026-02-07 15:42:55 [INFO] agent: Calling Claude with 60 tools
clawdbot  | 2026-02-07 15:43:07 [INFO] httpx: HTTP Request: POST https://api.anthropic.com/v1/messages "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:43:10 [INFO] httpx: HTTP Request: POST https://api.mem0.ai/v1/memories/ "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:43:10 [INFO] mem0-client: Stored 1 memories for user 980731551
clawdbot  | 2026-02-07 15:43:10 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:43:12 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/sendMessage "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:43:21 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:43:27 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:43:27 [INFO] handlers: Message from MOHIT (980731551): list of repos for my github...
clawdbot  | 2026-02-07 15:43:29 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/sendChatAction "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:43:31 [INFO] httpx: HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:43:31 [INFO] vectorstore: Added 1 documents to vector store
clawdbot  | 2026-02-07 15:43:34 [INFO] httpx: HTTP Request: POST https://api.mem0.ai/v2/memories/search/ "HTTP/1.1 400 Bad Request"
clawdbot  | 2026-02-07 15:43:34 [ERROR] mem0.client.utils: HTTP error occurred: Client error '400 Bad Request' for url 'https://api.mem0.ai/v2/memories/search/'
clawdbot  | For more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/400
clawdbot  | 2026-02-07 15:43:34 [ERROR] mem0-client: Failed to search memory: {"error":"Filters are required and cannot be empty. Please refer to https://docs.mem0.ai/api-reference/memory/search-memories"}
clawdbot  | 2026-02-07 15:43:34 [INFO] agent: Calling Claude with 60 tools
clawdbot  | 2026-02-07 15:43:40 [INFO] httpx: HTTP Request: POST https://api.anthropic.com/v1/messages "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:43:43 [INFO] httpx: HTTP Request: POST https://api.mem0.ai/v1/memories/ "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:43:43 [INFO] mem0-client: Stored 1 memories for user 980731551
clawdbot  | 2026-02-07 15:43:43 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:43:43 [WARNING] apscheduler.executors.default: Run time of job "TaskScheduler._check_pending_tasks (trigger: interval[0:01:00], next run at: 2026-02-07 15:44:37 UTC)" was missed by 0:00:06.127277
clawdbot  | 2026-02-07 15:43:44 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/sendMessage "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:43:53 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:44:04 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:44:16 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:44:17 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:44:17 [INFO] handlers: Message from MOHIT (980731551): https://github.com/Mohit-5899...
clawdbot  | 2026-02-07 15:44:19 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/sendChatAction "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:44:21 [INFO] httpx: HTTP Request: POST https://api.mem0.ai/v2/memories/search/ "HTTP/1.1 400 Bad Request"
clawdbot  | 2026-02-07 15:44:21 [ERROR] mem0.client.utils: HTTP error occurred: Client error '400 Bad Request' for url 'https://api.mem0.ai/v2/memories/search/'
clawdbot  | For more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/400
clawdbot  | 2026-02-07 15:44:21 [ERROR] mem0-client: Failed to search memory: {"error":"Filters are required and cannot be empty. Please refer to https://docs.mem0.ai/api-reference/memory/search-memories"}
clawdbot  | 2026-02-07 15:44:21 [INFO] agent: Calling Claude with 60 tools
clawdbot  | 2026-02-07 15:44:27 [INFO] httpx: HTTP Request: POST https://api.anthropic.com/v1/messages "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:44:27 [INFO] agent: Tool call: github_search_repositories({'query': 'user:Mohit-5899', 'perPage': 100})
clawdbot  | 2026-02-07 15:44:27 [INFO] agent: Executing tool: github_search_repositories
clawdbot  | 2026-02-07 15:44:27 [INFO] mcp-client: Executing MCP tool: github/search_repositories
clawdbot  | 2026-02-07 15:44:28 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:44:29 [ERROR] mcp-client: Request failed: MCP error: {'code': -32603, 'message': 'Authentication Failed: Bad credentials'}
clawdbot  | 2026-02-07 15:44:29 [ERROR] mcp-client: MCP tool execution failed: MCP error: {'code': -32603, 'message': 'Authentication Failed: Bad credentials'}
clawdbot  | 2026-02-07 15:44:29 [ERROR] agent: MCP tool failed: MCP error: {'code': -32603, 'message': 'Authentication Failed: Bad credentials'}
clawdbot  | 2026-02-07 15:44:37 [INFO] httpx: HTTP Request: POST https://api.anthropic.com/v1/messages "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:44:40 [INFO] httpx: HTTP Request: POST https://api.mem0.ai/v1/memories/ "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:44:40 [INFO] mem0-client: Stored 1 memories for user 980731551
clawdbot  | 2026-02-07 15:44:40 [WARNING] apscheduler.executors.default: Run time of job "TaskScheduler._check_pending_tasks (trigger: interval[0:01:00], next run at: 2026-02-07 15:45:37 UTC)" was missed by 0:00:03.499413
clawdbot  | 2026-02-07 15:44:40 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:44:42 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/sendMessage "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:44:51 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:45:01 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:45:12 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:45:22 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:45:33 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:45:37 [INFO] apscheduler.executors.default: Running job "TaskScheduler._check_pending_tasks (trigger: interval[0:01:00], next run at: 2026-02-07 15:46:37 UTC)" (scheduled at 2026-02-07 15:45:37.055516+00:00)
clawdbot  | 2026-02-07 15:45:37 [INFO] apscheduler.executors.default: Job "TaskScheduler._check_pending_tasks (trigger: interval[0:01:00], next run at: 2026-02-07 15:46:37 UTC)" executed successfully
clawdbot  | 2026-02-07 15:45:44 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:45:55 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:46:05 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:46:16 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:46:26 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:46:37 [INFO] apscheduler.executors.default: Running job "TaskScheduler._check_pending_tasks (trigger: interval[0:01:00], next run at: 2026-02-07 15:47:37 UTC)" (scheduled at 2026-02-07 15:46:37.055516+00:00)
clawdbot  | 2026-02-07 15:46:37 [INFO] apscheduler.executors.default: Job "TaskScheduler._check_pending_tasks (trigger: interval[0:01:00], next run at: 2026-02-07 15:47:37 UTC)" executed successfully
clawdbot  | 2026-02-07 15:46:37 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:46:47 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:46:58 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:47:08 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:47:19 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:47:29 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:47:37 [INFO] apscheduler.executors.default: Running job "TaskScheduler._check_pending_tasks (trigger: interval[0:01:00], next run at: 2026-02-07 15:48:37 UTC)" (scheduled at 2026-02-07 15:47:37.055516+00:00)
clawdbot  | 2026-02-07 15:47:37 [INFO] apscheduler.executors.default: Job "TaskScheduler._check_pending_tasks (trigger: interval[0:01:00], next run at: 2026-02-07 15:48:37 UTC)" executed successfully
clawdbot  | 2026-02-07 15:47:40 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:47:50 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:48:01 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:48:12 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:48:22 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:48:33 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:48:37 [INFO] apscheduler.executors.default: Running job "TaskScheduler._check_pending_tasks (trigger: interval[0:01:00], next run at: 2026-02-07 15:49:37 UTC)" (scheduled at 2026-02-07 15:48:37.055516+00:00)
clawdbot  | 2026-02-07 15:48:37 [INFO] apscheduler.executors.default: Job "TaskScheduler._check_pending_tasks (trigger: interval[0:01:00], next run at: 2026-02-07 15:49:37 UTC)" executed successfully
clawdbot  | 2026-02-07 15:48:44 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:48:54 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:49:04 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:49:15 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:49:25 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:49:35 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:49:37 [INFO] apscheduler.executors.default: Running job "TaskScheduler._check_pending_tasks (trigger: interval[0:01:00], next run at: 2026-02-07 15:50:37 UTC)" (scheduled at 2026-02-07 15:49:37.055516+00:00)
clawdbot  | 2026-02-07 15:49:37 [INFO] apscheduler.executors.default: Job "TaskScheduler._check_pending_tasks (trigger: interval[0:01:00], next run at: 2026-02-07 15:50:37 UTC)" executed successfully
clawdbot  | 2026-02-07 15:49:46 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:49:56 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:50:06 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:50:17 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:50:27 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:50:37 [INFO] apscheduler.executors.default: Running job "TaskScheduler._check_pending_tasks (trigger: interval[0:01:00], next run at: 2026-02-07 15:51:37 UTC)" (scheduled at 2026-02-07 15:50:37.055516+00:00)
clawdbot  | 2026-02-07 15:50:37 [INFO] apscheduler.executors.default: Job "TaskScheduler._check_pending_tasks (trigger: interval[0:01:00], next run at: 2026-02-07 15:51:37 UTC)" executed successfully
clawdbot  | 2026-02-07 15:50:37 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:50:48 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:50:58 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:51:08 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:51:19 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:51:29 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:51:37 [INFO] apscheduler.executors.default: Running job "TaskScheduler._check_pending_tasks (trigger: interval[0:01:00], next run at: 2026-02-07 15:52:37 UTC)" (scheduled at 2026-02-07 15:51:37.055516+00:00)
clawdbot  | 2026-02-07 15:51:37 [INFO] apscheduler.executors.default: Job "TaskScheduler._check_pending_tasks (trigger: interval[0:01:00], next run at: 2026-02-07 15:52:37 UTC)" executed successfully
clawdbot  | 2026-02-07 15:51:39 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:51:50 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:52:00 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:52:10 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:52:21 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:52:32 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:52:37 [INFO] apscheduler.executors.default: Running job "TaskScheduler._check_pending_tasks (trigger: interval[0:01:00], next run at: 2026-02-07 15:53:37 UTC)" (scheduled at 2026-02-07 15:52:37.055516+00:00)
clawdbot  | 2026-02-07 15:52:37 [INFO] apscheduler.executors.default: Job "TaskScheduler._check_pending_tasks (trigger: interval[0:01:00], next run at: 2026-02-07 15:53:37 UTC)" executed successfully
clawdbot  | 2026-02-07 15:52:42 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:52:48 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:52:48 [INFO] handlers: Message from MOHIT (980731551): can you schedule or set remiander at 11pm...
clawdbot  | 2026-02-07 15:52:49 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/sendChatAction "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:52:51 [INFO] httpx: HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:52:51 [INFO] vectorstore: Added 1 documents to vector store
clawdbot  | 2026-02-07 15:52:53 [INFO] httpx: HTTP Request: POST https://api.mem0.ai/v2/memories/search/ "HTTP/1.1 400 Bad Request"
clawdbot  | 2026-02-07 15:52:53 [ERROR] mem0.client.utils: HTTP error occurred: Client error '400 Bad Request' for url 'https://api.mem0.ai/v2/memories/search/'
clawdbot  | For more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/400
clawdbot  | 2026-02-07 15:52:53 [ERROR] mem0-client: Failed to search memory: {"error":"Filters are required and cannot be empty. Please refer to https://docs.mem0.ai/api-reference/memory/search-memories"}
clawdbot  | 2026-02-07 15:52:53 [INFO] agent: Calling Claude with 60 tools
clawdbot  | 2026-02-07 15:52:58 [INFO] httpx: HTTP Request: POST https://api.anthropic.com/v1/messages "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:52:59 [INFO] httpx: HTTP Request: POST https://api.mem0.ai/v1/memories/ "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:52:59 [INFO] mem0-client: Stored 1 memories for user 980731551
clawdbot  | 2026-02-07 15:52:59 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:53:01 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/sendMessage "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:53:10 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:53:20 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:53:30 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:53:37 [INFO] apscheduler.executors.default: Running job "TaskScheduler._check_pending_tasks (trigger: interval[0:01:00], next run at: 2026-02-07 15:54:37 UTC)" (scheduled at 2026-02-07 15:53:37.055516+00:00)
clawdbot  | 2026-02-07 15:53:37 [INFO] apscheduler.executors.default: Job "TaskScheduler._check_pending_tasks (trigger: interval[0:01:00], next run at: 2026-02-07 15:54:37 UTC)" executed successfully
clawdbot  | 2026-02-07 15:53:41 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:53:51 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:54:01 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:54:12 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:54:23 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:54:33 [INFO] httpx: HTTP Request: POST https://api.telegram.org/bot8468258015:AAFaC8YdALG2YcMUvTaeU7MQc71pcMuyCjk/getUpdates "HTTP/1.1 200 OK"
clawdbot  | 2026-02-07 15:54:37 [INFO] apscheduler.executors.default: Running job "TaskScheduler._check_pending_tasks (trigger: interval[0:01:00], next run at: 2026-02-07 15:55:37 UTC)" (scheduled at 2026-02-07 15:54:37.055516+00:00)
clawdbot  | 2026-02-07 15:54:37 [INFO] apscheduler.executors.default: Job "TaskScheduler._check_pending_tasks (trigger: interval[0:01:00], next run at: 2026-02-07 15:55:37 UTC)" executed successfully
clawdbot  | 2026-02-07 15:54:43 [INFO] httpx: HTTP Request: POST https://