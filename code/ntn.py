import tensorflow as tf
import params
import ntn_input
import random

# Inference
# Loss
# Training

def __init__(hyperparameters):
    # num_words           = hyperparameters['num_words']
    d = d          = hyperparameters['embedding_size']
    num_entities   = hyperparameters['num_entities']
    num_relations  = hyperparameters['num_relations']
    batch_size     = hyperparameters['batch_size']
    k = k          = hyperparameters['slice_size']
    corrupt_size   = hyperparameters['corrupt_size']
    # word_indices        = hyperparameters['word_indices']
    # activation_function = hyperparameters['activation_function']
    regularization = hyperparameters['lambda']

    # a 2D tensor with entity vectors. Someone needs to make this
    # and somehow we need to be able to index into it

    data_path = hyperparameters['data_path']
    entities_strings = ntn_input.load_entities(data_path)
    entity_to_index = {entities_strings[i] : i for i in len(entities_strings)}
    relation_strings = tf.constant(ntn_input.load_relations(data_path))
    relation_to_index = {relation_strings[i] : i for i in len(relation_strings)}

    (initEmbeds, entity_words) = ntn_input.load_init_embeds(data_path) 
    
    entity_words = entity_words #map from entity indices to list of word indices 
    W = W = dict()
    V = V = dict()
    b = b = dict()
    U = U = dict()
    E = E = tf.Variable(initEmbeds) #word embeddings

    examples = tf.placeholder(tf.float32, shape=(4, batch_size), name='batch')

    for r in relations:
        W[r] = tf.Variable(tf.truncated_normal([d, d, k])) # W[i] = np.random.random([d, d, k]) * 2 * r - r
        V[r] = tf.Variable(tf.zeros([2 * d, k]))
        b[r] = tf.Variable(tf.zeros([1, k]))
        U[r] = tf.Variable(tf.ones([k, 1]))


# e1 and e2 are d-dimensional entity vectors. W is a dxdxk tensor.
def bilinearTensorProduct(e1, W, e2):
    e1 = tf.reshape(e1, [1, d])
    W = tf.reshape(W, [d, d*k])
    temp = tf.matmul(e1, W)
    temp = tf.reshape(temp, [k, d])
    e2 = tf.reshape(e2, [d, 1])
    temp = tf.matmul(temp, e2)
    return temp

def g((e1, R, e2)):
    temp1 = bilinearTensorProduct(e1, W, e2)
    temp2 = tf.matmul(V, tf.concat(0, [e1, e2]))
    temp = tf.add(temp1, temp2, b)
    temp = tf.tanh(temp)
    temp = tf.matmul(U, temp)
    return temp

def L2():
    term = 0
    #sqrt(sum(trainable tensors))
    return term

# LOSS
def loss(batch, flip=True):        
    contrastive_max_margin = max(0.0, 1.0-g(true_triplet)+g(corrupt_triplet)) # + regularization term
    train_step = tf.train.AdagradOptimizer(0.01).minimize(contrastive_max_margin)

def train():
    training_strings = ntn_input.load_training_data()
    training_data = [(entity_to_index(entry[0]), relation_to_index(entry[1]), entity_to_index(entry[2])) for entry in training_strings]
    with tf.Session() as sess:
        init = tf.initialize_all_variables()
        sess.run(init)
        for i in range(iterations):
            batch = get_batch()
            sess.run(train_step, feed_dict={'batch':batch})

#returns a (batch_size*corrupt_size, 1) vector corresponding to g(T_c^i)-g(T^i) for all i
def inference(batch_placeholder, corrupt_placeholder, init_word_embeds,\
        entity_to_wordvec, num_entities, num_relations, slice_size):
    #TODO: We need to check the shapes and axes used here!
    d = 100 #embed_size
    k = slice_size
    E = tf.Variable(init_word_embeds, shape=(len(init_word_embeds), d)) #d=embed size
    W = [tf.Variable(tf.truncated_normal([d,d,k])) for r in range(len(num_relations))]
    V = [tf.Variable(tf.zeros([2 * d, k])) for r in range(len(num_relations))]
    b = [tf.Variable(tf.zeros([1, k])) for r in range(len(num_relations))]
    U = [tf.Variable(tf.ones([k, 1])) for r in range(len(num_relations))]


    e1, R, e2, e3 = tf.split(1, 4, batch_placeholder) #TODO: should the split dimension be 0 or 1? 
    #convert entity word index reps to embeddings... how?
    e1v = tf.reduce_mean(tf.gather(E, e1), 0)
    e2v = tf.reduce_mean(tf.gather(E, e2), 0)
    e3v = tf.reduce_mean(tf.gather(E, e3), 0)

    
    #e1v, e2v, e3v should be (batch_size * 100) tensors by now
    for r in range(num_relations):
        #get e1, e2, e3 cooresponding to indices where R[i] = r
        #TODO... uhh, stuff

            
def loss(infer_op):
    pass

def training(loss_op):
    pass
    

if __name__=="__main__":
    hyperparameters = {"data_path": params.data_path,
            "num_iter":             params.num_iter,
            "train_both":           params.train_both,
            "batch_size":           params.batch_size,
            "corrupt_size":         params.corrupt_size,
            "embedding_size":       params.embedding_size,
            "slice_size":           params.slice_size,
            "lambda":               params.reg_parameter,
            "in_tensor_keep_normal":params.in_tensor_keep_normal,
            "save_per_iter":        params.save_per_iter,
            "gradient_checking":    params.gradient_checking
        }
    ntn = NTN(hyperparameters)
