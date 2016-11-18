function [Matches] = MatchIdentify(States,Precomputed_States)
%This function is to identify all the matches that have similar
%states to the given state
ball=States.ball;
wicket=States.wicket;
run=States.run;
inning=States.inning;
Matches=[];
j=0;
% for i=2:size(Precomputed_States,1)
%     if ball==Precomputed_States{i,4} && wicket==Precomputed_States{i,5} && run==Precomputed_States{i,6} && inning==Precomputed_States{i,3}
%         j=j+1;
%         Matches{j,1}=Precomputed_States{i,1};
%     end
%     %if j>=1
%      %   if ball==Precomputed_States{i,4} && wicket==Precomputed_States{i,5} && run==Precomputed_States{i,5} && inning==Precomputed_States{i,3}
%       %      k=1;
%        % else
%         %    break;
%         %end
%     %end
% end
% More efficient way of doing this
% If the precomputed States is ordered one

for i=2:size(Precomputed_States,1)
    if ball==Precomputed_States{i,4} && wicket==Precomputed_States{i,5} && run==Precomputed_States{i,6} && inning==Precomputed_States{i,3}
        break;
    end
end

count=0;
for k=i:size(Precomputed_States,1)
    if ball==Precomputed_States{k,4} && wicket==Precomputed_States{k,5} && run==Precomputed_States{k,6} && inning==Precomputed_States{k,3}
        count=count + 1;
        Matches{count,1}=Precomputed_States{k,1};
    else
        break;
    end
end

end

