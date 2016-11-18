function [] = ImpEventIdentify(Input,Options)
% This function is to identify the imp events and returns the corre-
% -sponding matches in which such events have occurred previously.
% The inputs for this are as follows
% match_id: with the match_id corresponding excell File containing 
%           the ball by ball event details should be present in it.
%Probabilities: The excell file should contain the probabilities
%               for 1st and 2nd innings.
%Match_info: This is the file which contains all match details 
%            coressponding to each possible match_id
%Options: Theta: The value to identify the important event if 
%                difference in consecutive probabilities are
%                greater than theta.
%Note: The process is reading line by line so that  we can easily
%      adopt to the real time situation..

fprintf('Loading the required input files....\n')
match_id=strcat(Input.match_id,'.mat');
Probability1=strcat(Input.Probability1,'.mat');
Probability2=strcat(Input.Probability2,'.mat');
match_info=strcat(Input.match_info,'.mat');


load(match_id);
load(Probability1);
load(Probability2);
load(match_info);
load('PrecomputedStates.mat');
fprintf('Done\n');
Newmatch=match_details;
match_info=matchinfo;
ProbFirstInn=Probabilityfirstinnings;
ProbSecondInn=Probabilitysecondinnings;

fprintf('Running the algorithm to identify the Imp events...\n');

%First innings
fprintf('First Innings...\n');
Prev_State.ball=Newmatch{2,4};
Prev_State.wicket=not(isequal(Newmatch{2,5},'no_wicket'));
Prev_State.run=sum(cell2mat(Newmatch(2,6:10)));
Prev_State.inning=1;
Prev_Prob=Prob(Prev_State, ProbFirstInn);
count=0;
Probrealtime=zeros(size(Newmatch,1)-1,1);
Probrealtime(1)=Prev_Prob;
for i=3:size(Newmatch,1)
    if Newmatch{i,3}==1
        Current_State.ball=Newmatch{i,4};
        Current_State.wicket=Prev_State.wicket + not(isequal(Newmatch{i,5},'no_wicket'));
        Current_State.run=Prev_State.run + sum(cell2mat(Newmatch(i,6:10)));
        Current_State.inning=1;
        Current_Prob=Prob(Current_State, ProbFirstInn);
        Probrealtime(i-1)=Current_Prob;
        if abs(Current_Prob - Prev_Prob) > Options.theta
            count=count+1;
            Matches=MatchIdentify(Current_State, PrecomputedStates);
            if isempty(Matches)==0
                %Event_Match(:,count)=Matches;
                MatchInf(Matches,match_info,Current_State,Options.printnumber);
                fprintf('\n\n');
            end
        end
    else
        break;
    end
    Prev_State=Current_State;
    Prev_Prob=Current_Prob;
end
fprintf('Done...\n')

% Second Innings
fprintf('Second innings...\n')
i1st=i-1;
Prev_State.ball=Options.Maxball - Newmatch{i1st+1,4};
Prev_State.wicket=Options.Maxwicket - not(isequal(Newmatch{i1st+1,5},'no_wicket'));
Prev_State.run=Current_State.run - sum(cell2mat(Newmatch(i1st+1,6:10)));
Prev_State.inning=2;
Prev_Prob=Prob(Prev_State, ProbSecondInn);
Probrealtime(i1st)=1 - Prev_Prob;
for i=i1st+1:size(Newmatch,1)
    if Newmatch{i,3}==2
        Current_State.ball=Options.Maxball - Newmatch{i,4};
        Current_State.wicket=Prev_State.wicket - not(isequal(Newmatch{i,5},'no_wicket'));
        Current_State.run=Prev_State.run - sum(cell2mat(Newmatch(i,6:10)));
        Current_State.inning=2;
        Current_Prob=Prob(Current_State, ProbSecondInn);
        Probrealtime(i)=1 - Current_Prob;
        if abs(Current_Prob - Prev_Prob) > Options.theta
            count=count+1;
            Matches=MatchIdentify(Current_State, PrecomputedStates);
            if isempty(Matches)==0
                %Event_Match(:,count)=Matches;
                MatchInf(Matches,match_info,Current_State,Options.printnumber);
                fprintf('\n\n');
            end
        end
    else
        break;
    end
    Prev_State=Current_State;
    Prev_Prob=Current_Prob;
end

fprintf('Done...\n');

%New Figure
figure(1)
plot(1:size(Probrealtime),Probrealtime);
xlabel('As match proceeds')
ylabel('Probability of winning')
title('Probabilities in real time')
end

