#!/usr/bin/env escript
%% -*- erlang -*-
%%! -sname erl_lint

% stolen from https://github.com/sparr/erlint/blob/master/src/erlint.erl

main([]) ->
    ok;
main([Filename | Tail]) ->
    ok = handle_file(Filename),
    main(Tail).

handle_file(Filename) ->
    case lint(Filename) of
        {ok, Res} ->
            print(lists:sort(fun({_,F1,{L1,_,E1}},{_,F2,{L2,_,E2}}) -> {F1,L1,E1} =< {F2,L2,E2} end,Res));
        {error, Res} ->
            io:format("Error loading file: ~s~n",[file:format_error(Res)])
    end,
    ok.

lint(File) ->
    case epp:parse_file(File,[]) of
        {ok, Forms} ->
            {ok,
                case erl_lint:module(Forms, File) of
                    {ok, []} -> % nothing wrong
                        [];
                    {ok, Warnings} -> % just warnings
                        [ {warning,WFile,Warning} || {WFile,WList} <- Warnings, Warning <- WList ];
                    {error, Errors, []} -> % just errors
                        [ {error,EFile,Error} || {EFile,EList} <- Errors , Error <- EList ];
                    {error, Errors, Warnings} -> % errors and warnings
                        [ {error,EFile,Error} || {EFile,EList} <- Errors , Error <- EList ] ++
                        [ {warning,WFile,Warning} || {WFile,WList} <- Warnings, Warning <- WList ]
                end
            };
        {error, Err} ->
            {error, Err}
    end.

strip_newlines(Str) -> re:replace(Str,"[\\n\\r]","",[global]).

% degenerate case
print([]) ->
    ok;
print([{Type,File,{Line,Mod,Err}}|More]) ->
    io:fwrite("~s:~w: ~w: ~s~n",[File,Line,Type,strip_newlines(Mod:format_error(Err))]),
    print(More);
print(String) ->
    io:fwrite("~s~n",[String]).