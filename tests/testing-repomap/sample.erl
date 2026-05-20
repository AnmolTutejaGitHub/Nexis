-module(worker).
-behaviour(gen_server).
-export([start_link/0, process/1, get_state/0, stop/0]).
-export([init/1, handle_call/3, handle_cast/2, handle_info/2, terminate/2]).

start_link() ->
    gen_server:start_link({local, ?MODULE}, ?MODULE, #{}, []).

process(Task) ->
    gen_server:cast(?MODULE, {process, Task}).

get_state() ->
    gen_server:call(?MODULE, get_state).

stop() ->
    gen_server:stop(?MODULE).

init(State) ->
    {ok, State}.

handle_call(get_state, _From, State) ->
    {reply, State, State};
handle_call(_Req, _From, State) ->
    {reply, ok, State}.

handle_cast({process, Task}, State) ->
    NewState = maps:put(Task, done, State),
    {noreply, NewState};
handle_cast(_Msg, State) ->
    {noreply, State}.

handle_info(_Info, State) ->
    {noreply, State}.

terminate(_Reason, _State) ->
    ok.
