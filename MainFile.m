% This file is to identify the imp events that have occurred during
% the real time in match and give the similar matches in which this has
% occurred.
% This takes input as the match_id (new match), match_info,
% Probabilities for first and second innings.
% match_id: with the match_id corresponding excell File containing 
%           the ball by ball event details should be present in it.
%Probabilities: The excell file should contain the probabilities
%               for 1st and 2nd innings.
%Match_info: This is the file which contains all match details 
%            coressponding to each possible match_id

clc;
clear;
Input.match_id='clt_2009_01';
Input.Probability1='Probability_firstinnings';
Input.Probability2='Probability_secondinnings';
Input.match_info='match_info';

Options.theta=0.05;
Options.printnumber=10;
Options.Maxball=120;
Options.Maxwicket=10;
Options.Maxrun=250;
% diary on
% diary('Important Events clt_2009_01')
% ImpEventIdentify(Input,Options);
% diary off

Options.ball_delta=1;
Options.wicket_delta=1;
Options.run_delta=2;
Options.delta=15;
diary('Rare Events clt_2009_01')
frequency=RareEventIdentify(Input,Options);
diary off;