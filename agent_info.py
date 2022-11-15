from absl import flags

from dataclasses import dataclass
import numpy as np
import numpy.typing as npt

FLAGS = flags.FLAGS
flags.DEFINE_integer('num_agents', None, lower_bound=1, help='')
flags.mark_flag_as_required('num_agents')
flags.DEFINE_integer('num_class', None, lower_bound=1, help='')
flags.mark_flag_as_required('num_class')

@dataclass
class AgentConfig:
    alphas: npt.NDArray[np.float_]
    sigmas: npt.NDArray[np.float_]
    dists: list[npt.NDArray[np.float_]]
    start_coords: list[tuple]

def _gen_nclass(N, baseweight, topweight):
    norm = N*topweight + (FLAGS.num_class-N)*baseweight
    dists = list()
    for _ in range(FLAGS.num_agents):
        curr = np.ones(FLAGS.num_class)
        tops = np.random.choice(FLAGS.num_class, size=N, replace=False)
        for idx in tops:
            curr[idx] = topweight
        curr /= norm
        dists.append(curr)
    return AgentConfig(
        alphas=0.5 * np.ones(FLAGS.num_agents),
        sigmas=0.5 * np.ones(FLAGS.num_agents),
        dists=dists,
        start_coords=[(0, 0) for _ in range(FLAGS.num_agents)])


def getAgentConfig(mode):
    if mode == 'default':
        return AgentConfig(
            alphas=0.5*np.ones(FLAGS.num_agents),
            sigmas=0.5*np.ones(FLAGS.num_agents),
            dists=[np.ones(FLAGS.num_class)/FLAGS.num_class for _ in range(FLAGS.num_agents)],
            start_coords=[(0, 0) for _ in range(FLAGS.num_agents)])
    elif mode == 'nclass':
        return _gen_nclass(N=5, baseweight=1, topweight=4)
    elif mode == 'nclass-2':
        return _gen_nclass(N=3, baseweight=1, topweight=5)
    elif mode == 'nclass-3':
        return _gen_nclass(N=3, baseweight=1, topweight=10)
    elif mode == 'nclass-4':
        return _gen_nclass(N=3, baseweight=1, topweight=15)
    elif mode == 'extreme':
        dists = [np.zeros(FLAGS.num_class) for _ in range(FLAGS.num_agents)]
        tot = FLAGS.num_class
        per = tot // FLAGS.num_agents
        cls_count = [per] * FLAGS.num_agents
        left = tot - sum(cls_count)
        for i in range(left):
            cls_count[i] += 1

        for i in range(FLAGS.num_agents):
            pre = sum(cls_count[:i])
            dists[i][pre:pre+cls_count[i]] = 1 / cls_count[i]
        print(dists)

        return AgentConfig(
            alphas=0.5 * np.ones(FLAGS.num_agents),
            sigmas=0.5 * np.ones(FLAGS.num_agents),
            dists=dists,
            start_coords=[(0, 0) for _ in range(FLAGS.num_agents)])
    else:
        raise NotImplementedError(f"agent_info mode not implemented {mode}")
