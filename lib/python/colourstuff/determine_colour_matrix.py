"""PoC code to reverse-engineer an unknown colour-matrix applied to a
set of know pixel values
"""

import math
import array
import time
import random
import contextlib


@contextlib.contextmanager
def timeify(msg = ""):
    #print "[Start] %s" % msg
    start = time.time()
    yield
    end = time.time()
    print "%s %.04fms" % (msg, (end - start) * 1000)


def make_test_data(w = 128, h = 128):
    in_r, in_g, in_b = array.array('f'), array.array('f'), array.array('f')

    print "Make raw data"
    for x in range(w):
        for y in range(h):
            in_r.append(random.random())
            in_g.append(random.random())
            in_b.append(random.random())

    mtx = array.array('f', [random.random(), random.random(), random.random()])

    print "Matrixing"
    out_r = array.array('f', [(r*mtx[0] + g*mtx[1] + b*mtx[2]) for (r, g, b) in zip(in_r, in_g, in_b)])

    return {'in_r': in_r, 'in_g': in_g, 'in_b': in_b,
            'out_r': out_r,
            'mtx': mtx}


def score_matrix(ir, ig, ib, expect_r, mtx):
    ms = 0
    for i in range(len(ir)):
        val = ir[i] * mtx[0] + ig[i] * mtx[1] + ib[i] * mtx[2]
        ms += abs(val - expect_r[i]) ** 2
    rms = math.sqrt(ms / float(len(ir)))
    return rms


SOURCE = """
kernel void score_matrix_to_rms(
    global float* in_r,
    global float* in_g,
    global float* in_b,
    global float* expect_r,
    global float* score,
    int array_len,
    int cube_size
){
    float rm = 0;
    float val;

    int id = get_global_id(0);

    float mtx_r = (float)((id/cube_size/cube_size)%cube_size) / (cube_size-1);
    float mtx_g = (float)((id/cube_size)%cube_size) / (cube_size-1);
    float mtx_b = (float)((id)%cube_size) / (cube_size-1);

    for(int i = 0; i < array_len; ++i)
    {
        val = in_r[i] * mtx_r + in_g[i] * mtx_g + in_b[i] * mtx_b;
        rm += pow(fabs(expect_r[i] - val), 2);
    }

    score[id] = sqrt(rm/array_len);
}
"""

def setup_opencl(data, cube_size):
    import pycl

    with timeify("Making context, loading kernel"):
        devices = pycl.clGetDeviceIDs()
        ctx = pycl.clCreateContext(devices = devices)
        queue = pycl.clCreateCommandQueue(ctx)

        program = pycl.clCreateProgramWithSource(ctx, SOURCE).build()

        score_matrix = program['score_matrix_to_rms']
        score_matrix.argtypes = (pycl.cl_mem, pycl.cl_mem, pycl.cl_mem,
                                 pycl.cl_mem, pycl.cl_mem, pycl.cl_int, pycl.cl_int)

    sub_divisions = cube_size**3

    with timeify("Creating buffers"):
        in_r_buf, in_evt1 = pycl.buffer_from_pyarray(queue, data['in_r'], blocking = False)
        in_g_buf, in_evt2 = pycl.buffer_from_pyarray(queue, data['in_g'], blocking = False)
        in_b_buf, in_evt3 = pycl.buffer_from_pyarray(queue, data['in_b'], blocking = False)

        out_r = data['out_r']
        out_r_buf, in_evt4 = pycl.buffer_from_pyarray(queue, out_r, blocking = False)

        score = array.array('f', [0 for x in range(sub_divisions)])
        score_buf, in_evt5 = pycl.buffer_from_pyarray(queue, score, blocking = False)


    with timeify("Run kernel"):
        run_evt = score_matrix(
            in_r_buf, in_g_buf, in_b_buf, out_r_buf, score_buf,
            len(data['in_r']), cube_size,
            wait_for = [in_evt1, in_evt2, in_evt3, in_evt4, in_evt5]).on(queue,
                                                                         sub_divisions)

    with timeify("Retrive data"):
        score_from_gpu, evt = pycl.buffer_to_pyarray(queue, score_buf,
                                                     wait_for=run_evt,
                                                     like=score)

    return score_from_gpu


if __name__ == '__main__':
    def index_to_rgb(i, cube_size):
        r = float( ((i/cube_size/cube_size)%cube_size) ) / (cube_size-1)
        g = float( ((i/cube_size)%cube_size) ) / (cube_size-1)
        b = float( ((i)%cube_size) ) / (cube_size-1)

        return (r, g, b)

    print "OpenCL matrix guesser"
    img_size = 8

    cube_size = 256 + 128

    with timeify("Make test data"):
        data = make_test_data(w = img_size, h = img_size)

    with timeify("OpenCL impl"):
        from_cl = setup_opencl(data, cube_size = cube_size)

    with timeify("Get lowest value"):
        closest = min(from_cl)

    """
    with timeify("CPU"):
        from_py = score_matrix(data['in_r'], data['in_g'], data['in_b'], data['out_r'], mtx = new_mtx)

    dif = abs(from_py - from_cl)
    print "cl: %.10f\npy: %.10f\nDiff: %.10f" % (from_cl, from_py, dif)
    """

    print "secret test matrix was", "%.04f %.04f %.04f" % tuple(data['mtx'].tolist())
    print "Closest                ", "%.04f %.04f %.04f" % index_to_rgb(from_cl.index(closest), cube_size = cube_size)
