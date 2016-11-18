function [frequency] = RareEventIdentify(Input, Options)
% This is a function that is used to identify the events that are 
% rare in real time.
%
% We classify an event as rare if the neighbourhood ball containing 
% this event has less number of occurrencies in the past (frequency)
%
% This function takes the following inmputs.
% Input:
% match_id: with the match_id corresponding excell File containing 
%           the ball by ball event details should be present in it.
%
% Options:
%  We consider a tolerance level on each elemnt of the state space
%  and look the frequencies in these tolerances.
%  ball_delta= Represents balls(+-) ball_delta
%  wicket_delta = Represents wickets(+-) wicket_delta
%  Run_delta = Represents runs (+-) run_delta
%  delta= represents the threshold frequency limit, below which 
%         we can clssify it as rare event.
%
% Note: The process is reading line by line so that  we can easily
%       adopt to the real time situation..

fprintf('Loading the required input files....\n')

match_id=strcat(Input.match_id,'.mat');
match_info=strcat(Input.match_info,'.mat');


load(match_id);
load(match_info);
load('PrecomputedStates.mat');

fprintf('Done\n');

Newmatch=match_details;
fprintf('Running the algorithm to identify the rare events...\n\n');

frequency{1,1}='ball';
frequency{1,2}='wicket';
frequency{1,3}='run';
frequency{1,4}='innings';
frequency{1,5}='Frequency of occurrence';
Prev_State.run=0;
Prev_State.wicket=0;
for i=2:size(Newmatch,1)
        if Newmatch{i,3}==1
            State.ball=Newmatch{i,4};
            State.wicket=Prev_State.wicket + not(isequal(Newmatch{i,5},'no_wicket'));
            State.run=Prev_State.run + sum(cell2mat(Newmatch(i,6:10)));
            State.inning=1;
        else
            if Prev_State.inning ~= 2
                Prev_State.wicket=Options.Maxwicket;
            end
            State.ball=Options.Maxball - Newmatch{i,4};
            State.wicket=Prev_State.wicket - not(isequal(Newmatch{i,5},'no_wicket'));
            State.run=Prev_State.run - sum(cell2mat(Newmatch(i,6:10)));
            State.inning=2;
        end
        frequency{i,1}=State.ball;
        frequency{i,2}=State.wicket;
        frequency{i,3}=State.run;
        frequency{i,4}=State.inning;
        frequency{i,5}=0;
        count=0;
        for i1=-Options.ball_delta:Options.ball_delta
            for i2=-Options.wicket_delta:Options.wicket_delta
                for i3=-Options.run_delta:Options.run_delta
                    Surr_State.ball=State.ball + i1;
                    Surr_State.wicket=State.wicket + i2;
                    Surr_State.run=State.run + i3;
                    Surr_State.inning=State.inning;
                    if Surr_State.ball <= Options.Maxball && Surr_State.wicket <= Options.Maxwicket && Surr_State.run<= Options.Maxrun
                        if Surr_State.ball >=0 && Surr_State.wicket >=0 && Surr_State.run >=0
                            count=count+1;
                            Matches=[];
                            Matches=MatchIdentify(Surr_State, PrecomputedStates);
                            frequency{i,5}=cell2mat(frequency(i,5)) + size(Matches,1);
                            %if cell2mat(frequency(i,4)) > Options.delta
                             %   frequency{i,4}='Frequency greter than threshold';
                              %  break;
                            %end
                        end
                    end
                end
                %if cell2mat(frequency(i,4)) > Options.delta
                 %   break;
                %end
            end
            %if cell2mat(frequency(i,4)) > Options.delta
             %   break;
            %end
        end
        fprintf('The current state is (%i, %i,%i)\n',State.ball,State.wicket,State.run); 
        % Printing the output
        if cell2mat(frequency(i,5)) < Options.delta
            fprintf('This state of (%i, %i, %i) in %i innings is a rare event.\n',...
                State.ball,State.wicket,State.run,State.inning)
            fprintf('The frequency of occurences in the neighbourhood of this state is %i.\n\n',cell2mat(frequency(i,5)))
        end
        Prev_State=State;
end

fprintf('Done...\n')

end

