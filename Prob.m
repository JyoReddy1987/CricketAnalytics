function [ Probability ] = Prob(State, ProbInn)
%This function is to identify the probability of the given state
%from the previously computed states.
% Inputs:
% States: Containing (b,w,r)
% Matrix; Containing the probabilities
Probability=1;
for i=2:size(ProbInn,1)
    if (State.ball==cell2mat(ProbInn(i,2)) && State.wicket==cell2mat(ProbInn(i,1)) && State.run==cell2mat(ProbInn(i,3)))
        Probability=ProbInn{i,4};
        break;
    end
end
    


end

