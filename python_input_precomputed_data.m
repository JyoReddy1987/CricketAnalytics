% This file is to calculate the precomputed excell file which
% is given as input for the python script...This file has states
% and events in each given match.
clc;
clear;

Max_balls=120;
Max_wickets=10;
load('TWENTY20.mat');

Match=TWENTY20;
[~,index] = unique(Match(1:end,1));
match_id=Match(sort(index),1);

States_Array=Match(:,[1 2 3 4]);
States_Array{1,4}='balls';
States_Array{1,5}='wickets';
States_Array{1,6}='runs';

j1=2;
for i=2:size(match_id,1)
    for j=j1:size(Match,1)
        
        %First Innings
        if strcmpi(match_id(i), Match{j,1})== 1 && Match{j,3}==1
            States_Array{j,7}=not(isequal(Match{j,5},'no_wicket'));
            States_Array{j,5}=sum(cell2mat(States_Array(j1:j,7)));
            States_Array{j,6}=sum(sum(cell2mat(Match(j1:j,6:10))));
            j1st=j;
            
        %Second Innings
        elseif strcmpi(match_id(i), Match{j,1})== 1 && Match{j,3}==2
            States_Array{j,4}=Max_balls - States_Array{j,4};
            States_Array{j,7}=not(isequal(Match{j,5},'no_wicket'));
            States_Array{j,5}=Max_wickets - sum(cell2mat(States_Array(j1st+1:j,7)));
            %States_Array{j,5}=Max_wickets - sum(~cellfun('isempty',Match(j1st+1:j,11)));
            States_Array{j,6}= States_Array{j1st,6} - sum(sum(cell2mat(Match(j1st+1:j,6:10))));
            if States_Array{j,6}<0
                States_Array{j,6}=0;
            end
        else
            break;
        end
    end
    j1=j;
end
States_Array(:,7)=[];
%filename='Precomputed_States.xlsx';
%xlswrite(States_Array,filename);

States.ball=1;
States.wicket=0;
States.run=6;
States.inning=1;
Matches=MatchIdentify(States,States_Array);

load('match_info.mat');
%MatchData=MatchInf(Matches, match_info,States,printnumber);
        
    