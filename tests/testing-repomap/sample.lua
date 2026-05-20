local M = {}
local json = require("cjson")

function M.create_server(host, port)
    return {
        host = host,
        port = port,
        running = false,
    }
end

function M.send_request(server, path, method)
    method = method or "GET"
    if not server.running then
        return nil, "server not running"
    end
    return { status = 200, path = path, method = method }
end

function M.parse_response(data)
    if type(data) == "string" then
        return json.decode(data)
    end
    return data
end

function M.start(server)
    server.running = true
    return server
end

function M.stop(server)
    server.running = false
end

return M
