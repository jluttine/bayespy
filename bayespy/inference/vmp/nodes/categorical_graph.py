################################################################################
# Copyright (C) 2017 Jaakko Luttinen
#
# This file is licensed under the MIT License.
################################################################################


class CategoricalGraphMoments(Moments):


    def __init__(self):
        raise NotImplementedError()


    def compute_fixed_moments(self, x):
        raise NotImplementedError()


    @classmethod
    def from_values(cls, x):
        raise NotImplementedError()


class CategoricalGraphDistribution(Distribution):


    def __init__(self):
        raise NotImplementedError()


    def compute_message_to_parent(self, parent, index, u, *u_parents):
        raise NotImplementedError()


    def compute_phi_from_parents(self, *u_parents, mask=True):
        raise NotImplementedError()


    def compute_moments_and_cgf(self, phi, mask=True):
        raise NotImplementedError()


    def compute_cgf_from_parents(self, *u_parents):
        raise NotImplementedError()


    def compute_fixed_moments_and_f(self, x, mask=True):
        raise NotImplementedError()


    def random(self, *phi, plates=None):
        raise NotImplementedError()


    def compute_gradient(self, g, u, phi):
        raise NotImplementedError()


class CategoricalGraph():
    """

    X = CategoricalGraph(
        [
            Variable(
                table=[0.8, 0.2],
            ),
            Variable(
                table=[[0.6, 0.4], [0.99, 0.01]],
                given=[0],
                plates=['lawns']
            ),
            Variable(
                table=[ [[1.0, 0.0], [0.2, 0.8]],
                        [[0.1, 0.9], [0.01, 0.99]] ],
                given=[0, 1],
                plates=['lawns']
            ),
        ]
        {
            'rain': [0.8, 0.2],
            'sprinkler': dict(table=[[0.6, 0.4], [0.99, 0.01]],
                            given=['rain'],
                            plates=['lawns'],
                            platemap="i->i"),
            'grass wet': dict(table=[ [[1.0, 0.0], [0.2, 0.8]],
                                    [[0.1, 0.9], [0.01, 0.99]] ],
                            given=['sprinkler', 'rain'],
                            plates=['lawns'],
                            platemap="i->i")
        },
        plates={
            'lawns': 10,
        },
        # If needed, one could explicitly give a mapping from the graph plates
        # to plate axes of other BayesPy nodes:
        # NO! Use platemap attribute in the Variable class!
        plates_axes={
            'lawns': 0,
        },
    )

    Hmm.. How to get a child node with arbitrary (joint) marginals?

    X[['rain','sprinkler'],['rain']] ?

    """


    def __init__(self, dag, plates={}):
        factorgraph = [
            variable.given + [name]
            for (name, variable) in dag.items()
        ]
        sizes = {
            name: np.shape(variable.table)[-1]
            for name in dag.keys()
        }
        # FIXME: Here we just assume fixed arrays as CPTs, not Dirichlet nodes
        self._cpts = [
            variable.table
            for variable in dag.values()
        ]
        self._junctiontree = jt.create_junction_tree(factorgraph, sizes)
        # TODO: Call super?
        return


    def lower_bound_contribution(self):
        raise NotImplementedError()


    def get_moments(self):
        return self.u


    def update(self):
        # TODO: Fetch CPTs from Dirichlet parents and make use of potentials
        # from children.
        self.u = self._junctiontree.propagate(self._cpts)
        return
