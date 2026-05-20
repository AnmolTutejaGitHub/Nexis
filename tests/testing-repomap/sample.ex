defmodule MyApp.Router do
  use Plug.Router

  plug :match
  plug :dispatch

  get "/health" do
    send_resp(conn, 200, "ok")
  end

  post "/users" do
    send_resp(conn, 201, "created")
  end

  def start_link(opts \\ []) do
    {:ok, self()}
  end

  def child_spec(opts) do
    %{id: __MODULE__, start: {__MODULE__, :start_link, [opts]}}
  end
end

defmodule MyApp.Worker do
  use GenServer

  def init(state), do: {:ok, state}

  def handle_call(:get, _from, state), do: {:reply, state, state}

  def handle_cast({:set, val}, _state), do: {:noreply, val}
end
