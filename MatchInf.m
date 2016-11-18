function [Info] = MatchInf(Matches,match_info,States,printnumber)
%This function is to print and give the information of the given
%matches.
%Input:
%Matches=       Cells containing match id's
%match_info=    This is the cell structure containing all the 
%               information about the matches played
%States=        States consist of (ball,wicket,runs) and innings
%               
%printnumber=   Maximum number of matches information that can 
%               be printed


Info(1,:)=match_info(1,:);
for i=1:size(Matches,1)
    for j=2:size(match_info,1)
        if strcmpi(Matches{i,1},match_info{j,1})==1
            Info(i+1,:)=match_info(j,:);
        end
    end
end

%Printing the output
fprintf('This is an Important event.\n')
fprintf('State (%i,%i,%i) in %i innings has occurred in previously\n', States.ball,States.wicket,States.run,States.inning)
fprintf('played matches. The following gives information about such matches\n')

max_print=min(printnumber, size(Info,1)-1);
for k=2:max_print+1
    if strcmpi(Info{k,9},'Team1')
        Team=Info{k,2};
        Team=strcat(Team, ' have won the match');
    elseif strcmpi(Info{k,9},'Team2')
        Team=Info{k,3};
        Team=strcat(Team, ' have won the match');
    elseif strcmpi(Info{k,9},'Tie')
        Team=' the match was a tie';
    else
        Team=' got no result at the end of the game';
    end
    if States.inning==1
        fprintf('%i. %s vs %s played at %s on %s in which %s was at state (%i, %i, %i) in First innings and finally %s\n',k-1,...
        Info{k,2}, Info{k,3}, Info{k,4},Info{k,5}, Info{k,2},States.ball,States.wicket,States.run,Team);
    else
        fprintf('%i. %s vs %s played at %s on %s in which %s was at state (%i, %i, %i) in Second innings and finally %s\n',k-1,...
        Info{k,2}, Info{k,3}, Info{k,4},Info{k,5}, Info{k,3},States.ball,States.wicket,States.run,Team);
    end
end

end

