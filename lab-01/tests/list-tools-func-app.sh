curl -X POST https://telco-mcp-func-app-fjadhdg3gjffdyh8.westus2-01.azurewebsites.net/runtime/webhooks/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{
    "jsonrpc": "2.0",
    "id": 4,
    "method": "tools/list",
    "params": {
    }
  }'
