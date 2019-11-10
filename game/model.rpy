init -1 python:
    def cumsum(lst):
        """
        Function to calculate the cumulative sum, replacing the one in NumPy
        """
        return [sum(lst[0:x+1]) for x in range(0,len(lst))]

    class Patient():
        '''
        Simulate the mental state of a patient with bipolar disorder
        using Markov chain, each time step is one week.
        '''
        def __init__(self, std=0.01, p_relapse=0.01, p_recovery=0.2, init_prob=None, matrix=None):
            '''
            Inputs:

                std (float) The standard deviation when sampling noise from a distribution.
                  Default: 0.01.

                p_relapse (float) The probability of relapse after recovery at each
                  time step (one week), i.e. the probability that state 0 at time t
                  will move to another state at time t+1. Default: 0.01.

                p_recovery (float) The probability of recovery if transitioning
                  to state 0 during cycling. Default: 0.2.

                init_prob (list) The probability of the initial state. We assume that
                  we never start from state 0. Default: None

                matrix (dict) The transition matrix in the form of a dict. Each key
                  has a list containing probability transitioning to another state.
                  The possible states are -2, -1, 1, 2, and 0, in that order, but
                  probability to transition to state 0 is implied to be the complement
                  of the other probabilities. Default: None.
                  '''
            if matrix:
                self._matrix = matrix
            else:
                self._matrix = {-2: [0.93, 0, 0.004, 0.004],
                               -1: [0, 0.835, 0.017, 0.028],
                               1: [0.04, 0.065, 0.67, 0],
                               2: [0.011, 0.011, 0, 0.855]}
            self._std = std
            self._p_relapse = p_relapse
            self._p_recovery = p_recovery
            # Randomize initial state
            if init_prob:
                self._init_prob = init_prob
            else:
                self._init_prob = [0.38, 0.19, 0.17, 0.26]
            self._state = NonUniformRandom([-2, -1, 1, 2], self._init_prob).pick()
            self._length = 0 # length of an episode
            self._path = [] # list to record changing mental states in an episode
            self._episodes = [] # list to record lengths of all episodes in this simulation
            self._episode_type = [] # list to record type of all episodes in this simulation

        def _sample_prob(self, mean, mu=None):
            """Add noise to the probability"""
            if mu:
                return skew_random(mean, mu)
            else:
                return skew_random(mean, self._std)

        def _update(self, reroll=True):
            """Update the state of the patient"""
            # Get the transition probabilities for this state

            transition = self._matrix[self._state]
            cum_sum = cumsum(transition)
            p = renpy.random.random()
            if p < self._sample_prob(cum_sum[0], transition[0]):
                self._state = -2
            elif p < self._sample_prob(cum_sum[1], transition[1]):
                self._state = -1
            elif p < self._sample_prob(cum_sum[2], transition[2]):
                self._state = 1
            elif p < self._sample_prob(cum_sum[3], transition[3]):
                self._state = 2
            # If the type of the episode is 4 or 5 (cycling), then there is a chance
            # to get another "roll"
            elif self._check_type() > 3 and reroll and renpy.random.random() > self._sample_prob(self._p_recovery):
                    self._update(False)
            else:
              # An episode ends only if the person experiences at least 8 consecutive weeks
              # with no symptoms
                count = 0
              # Go for 8 weeks, each with a chance of relapse
                while count < 8 and renpy.random.random() > self._sample_prob(2*self._p_relapse):
                    count += 1
              # If the while loop ends on 8 weeks, then the episode ends and the person
              # has recovered
                if count >= 8:
                    self._state = 0
              # If the while loop ends early, it means they relapsed. Return to their
              # most recent state and add the weeks advanced to length of episode
                else:
                    self._length += count

        def _check_type(self):
            """Check the type of the episode"""
            # -1 if no episode
            if self._length == 0:
                return -1
            # Major depression (0) if the person has major depression (-2) throughout
            if all([x == -2 for x in self._path]):
                return 0
            # Minor depression (1) if the person has minor depression (-1) throughout
            if all([x == -1 for x in self._path]):
                return 1
            # Mania (2) if the person is manic (2) throughout
            if all([x == 2 for x in self._path]):
                return 2
            # Hypomania (3) if the person is hypomanic (1) throughout
            if all([x == 1 for x in self._path]):
                return 3
            # Minor cycling (4) if the person is swings between minor depression and hypomania
            if all([abs(x) == 1 for x in self._path]):
                return 4
            # Else, major cycling.
            return 5

        # Methods added for the game
        def get_state(self):
            """Retrieve current state for front-end"""
            return self._state

        def get_new_state(self):
            """Simulate and return the next state"""
            if self._state == 0:
                if renpy.random.random() < self._sample_prob(self._p_relapse):
                    self._state = NonUniformRandom([-2, -1, 1, 2], self._init_prob).pick()
            else:
                self._update()
            return self._state

        # Methods from this point on are used only for analysis and not in the game
        def simulate_single(self):
            """Simulate a single episode"""
            while self._state != 0:
                self._length += 1
                self._path.append(self._state)
                self._update()

        def simulate(self, steps):
            """Simulate for a desired amount of time"""
            count = 0
            while count < steps:
                count += 1
                # If having symptoms, then follow the same steps in the single episode simulation
                if self._state != 0:
                    self._length += 1
                    self._path.append(self._state)
                    self.update()
                # If recovered:
                else:
                    # Only count the episode if it lasts at least 2 weeks
                    if self._length >= 2:
                        self._episodes.append(self._length)
                        self._episode_type.append(self._check_type())
                    # Reset episode
                    self._length = 0
                    self._path = []
                    # If the person relapse, re-initialize from beginning
                    if renpy.random.random() < self._sample_prob(self._p_relapse):
                        self._state = NonUniformRandom([-2, -1, 1, 2], self._init_prob).pick()
