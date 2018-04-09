from pylab import *
import util
import numpy as np


class Candidate:
    votes = []
    prev_vote = 0
    pitch = 0
    no_votes = 0

    def __init__(self):
        self.votes = []
        self.prev_vote = 0
        self.pitch = 0
        self.no_votes = 0

    def add_vote(self, vote):
        self.prev_vote = vote
        self.votes.append(vote)
        self.no_votes = len(self.votes)
        self.pitch = np.mean(self.votes)


def find_est_candidate(estimation_list):
    can_list = [[]]
    for est in estimation_list:
        found = False
        for can in can_list:
            if can == []:
                can.append(est)
                found = True
            elif est == can[0]:
                can.append(est)
                found = True
            elif not found:
                can_list.append([est])
    index = argmax(len(can) for can in can_list)
    final_can = can_list[index]
    return final_can


def find_pitch_candidate(value_list, min_value):
    can_list = []
    current_can = Candidate()
    for value in value_list:
        if value > min_value:
            # add first pitch as candidate
            if len(can_list) == 0:
                can = Candidate()
                can.add_vote(value)
                can_list.append(can)
                current_can = can
            else:
                prev_vote = current_can.prev_vote
                # does the current pitch match with the previous candidate
                if util.in_scope(value, prev_vote):
                    current_can.add_vote(value)
                else:
                    # find matching pre-existent candidate
                    has_can = False
                    for can in can_list:
                        if util.in_scope(value, can.pitch):
                            has_can = True
                            can.add_vote(value)
                            current_can = can
                    # create new candidate if none matches
                    if not has_can:
                        can = Candidate()
                        can.add_vote(value)
                        can_list.append(can)
                        current_can = can
    final_candidate = Candidate()
    # find candidate with the most votes
    for can in can_list:
        if can.no_votes > final_candidate.no_votes:
            final_candidate = can
    return final_candidate.pitch


def make_candidate():
    return Candidate()
