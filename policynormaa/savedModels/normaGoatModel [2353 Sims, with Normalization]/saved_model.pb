ұ
��
^
AssignVariableOp
resource
value"dtype"
dtypetype"
validate_shapebool( �
�
BiasAdd

value"T	
bias"T
output"T""
Ttype:
2	"-
data_formatstringNHWC:
NHWCNCHW
8
Const
output"dtype"
valuetensor"
dtypetype
$
DisableCopyOnRead
resource�
.
Identity

input"T
output"T"	
Ttype
\
	LeakyRelu
features"T
activations"T"
alphafloat%��L>"
Ttype0:
2
u
MatMul
a"T
b"T
product"T"
transpose_abool( "
transpose_bbool( "
Ttype:
2	
�
MergeV2Checkpoints
checkpoint_prefixes
destination_prefix"
delete_old_dirsbool("
allow_missing_filesbool( �

NoOp
M
Pack
values"T*N
output"T"
Nint(0"	
Ttype"
axisint 
C
Placeholder
output"dtype"
dtypetype"
shapeshape:
@
ReadVariableOp
resource
value"dtype"
dtypetype�
o
	RestoreV2

prefix
tensor_names
shape_and_slices
tensors2dtypes"
dtypes
list(type)(0�
l
SaveV2

prefix
tensor_names
shape_and_slices
tensors2dtypes"
dtypes
list(type)(0�
?
Select
	condition

t"T
e"T
output"T"	
Ttype
H
ShardedFilename
basename	
shard

num_shards
filename
�
StatefulPartitionedCall
args2Tin
output2Tout"
Tin
list(type)("
Tout
list(type)("	
ffunc"
configstring "
config_protostring "
executor_typestring ��
@
StaticRegexFullMatch	
input

output
"
patternstring
L

StringJoin
inputs*N

output"

Nint("
	separatorstring 
�
VarHandleOp
resource"
	containerstring "
shared_namestring "
dtypetype"
shapeshape"#
allowed_deviceslist(string)
 �"serve*2.14.02v2.14.0-rc1-21-g4dacf3f368e8��
�
training/Adam/dense_5/bias/vVarHandleOp*
_output_shapes
: *
dtype0*
shape:y*-
shared_nametraining/Adam/dense_5/bias/v
�
0training/Adam/dense_5/bias/v/Read/ReadVariableOpReadVariableOptraining/Adam/dense_5/bias/v*
_output_shapes
:y*
dtype0
�
training/Adam/dense_5/kernel/vVarHandleOp*
_output_shapes
: *
dtype0*
shape
:9y*/
shared_name training/Adam/dense_5/kernel/v
�
2training/Adam/dense_5/kernel/v/Read/ReadVariableOpReadVariableOptraining/Adam/dense_5/kernel/v*
_output_shapes

:9y*
dtype0
�
training/Adam/dense_4/bias/vVarHandleOp*
_output_shapes
: *
dtype0*
shape:9*-
shared_nametraining/Adam/dense_4/bias/v
�
0training/Adam/dense_4/bias/v/Read/ReadVariableOpReadVariableOptraining/Adam/dense_4/bias/v*
_output_shapes
:9*
dtype0
�
training/Adam/dense_4/kernel/vVarHandleOp*
_output_shapes
: *
dtype0*
shape
:F9*/
shared_name training/Adam/dense_4/kernel/v
�
2training/Adam/dense_4/kernel/v/Read/ReadVariableOpReadVariableOptraining/Adam/dense_4/kernel/v*
_output_shapes

:F9*
dtype0
�
training/Adam/dense_3/bias/vVarHandleOp*
_output_shapes
: *
dtype0*
shape:F*-
shared_nametraining/Adam/dense_3/bias/v
�
0training/Adam/dense_3/bias/v/Read/ReadVariableOpReadVariableOptraining/Adam/dense_3/bias/v*
_output_shapes
:F*
dtype0
�
training/Adam/dense_3/kernel/vVarHandleOp*
_output_shapes
: *
dtype0*
shape
:RF*/
shared_name training/Adam/dense_3/kernel/v
�
2training/Adam/dense_3/kernel/v/Read/ReadVariableOpReadVariableOptraining/Adam/dense_3/kernel/v*
_output_shapes

:RF*
dtype0
�
training/Adam/dense_5/bias/mVarHandleOp*
_output_shapes
: *
dtype0*
shape:y*-
shared_nametraining/Adam/dense_5/bias/m
�
0training/Adam/dense_5/bias/m/Read/ReadVariableOpReadVariableOptraining/Adam/dense_5/bias/m*
_output_shapes
:y*
dtype0
�
training/Adam/dense_5/kernel/mVarHandleOp*
_output_shapes
: *
dtype0*
shape
:9y*/
shared_name training/Adam/dense_5/kernel/m
�
2training/Adam/dense_5/kernel/m/Read/ReadVariableOpReadVariableOptraining/Adam/dense_5/kernel/m*
_output_shapes

:9y*
dtype0
�
training/Adam/dense_4/bias/mVarHandleOp*
_output_shapes
: *
dtype0*
shape:9*-
shared_nametraining/Adam/dense_4/bias/m
�
0training/Adam/dense_4/bias/m/Read/ReadVariableOpReadVariableOptraining/Adam/dense_4/bias/m*
_output_shapes
:9*
dtype0
�
training/Adam/dense_4/kernel/mVarHandleOp*
_output_shapes
: *
dtype0*
shape
:F9*/
shared_name training/Adam/dense_4/kernel/m
�
2training/Adam/dense_4/kernel/m/Read/ReadVariableOpReadVariableOptraining/Adam/dense_4/kernel/m*
_output_shapes

:F9*
dtype0
�
training/Adam/dense_3/bias/mVarHandleOp*
_output_shapes
: *
dtype0*
shape:F*-
shared_nametraining/Adam/dense_3/bias/m
�
0training/Adam/dense_3/bias/m/Read/ReadVariableOpReadVariableOptraining/Adam/dense_3/bias/m*
_output_shapes
:F*
dtype0
�
training/Adam/dense_3/kernel/mVarHandleOp*
_output_shapes
: *
dtype0*
shape
:RF*/
shared_name training/Adam/dense_3/kernel/m
�
2training/Adam/dense_3/kernel/m/Read/ReadVariableOpReadVariableOptraining/Adam/dense_3/kernel/m*
_output_shapes

:RF*
dtype0
b
count_1VarHandleOp*
_output_shapes
: *
dtype0*
shape: *
shared_name	count_1
[
count_1/Read/ReadVariableOpReadVariableOpcount_1*
_output_shapes
: *
dtype0
b
total_1VarHandleOp*
_output_shapes
: *
dtype0*
shape: *
shared_name	total_1
[
total_1/Read/ReadVariableOpReadVariableOptotal_1*
_output_shapes
: *
dtype0
�
training/Adam/learning_rateVarHandleOp*
_output_shapes
: *
dtype0*
shape: *,
shared_nametraining/Adam/learning_rate
�
/training/Adam/learning_rate/Read/ReadVariableOpReadVariableOptraining/Adam/learning_rate*
_output_shapes
: *
dtype0
z
training/Adam/decayVarHandleOp*
_output_shapes
: *
dtype0*
shape: *$
shared_nametraining/Adam/decay
s
'training/Adam/decay/Read/ReadVariableOpReadVariableOptraining/Adam/decay*
_output_shapes
: *
dtype0
|
training/Adam/beta_2VarHandleOp*
_output_shapes
: *
dtype0*
shape: *%
shared_nametraining/Adam/beta_2
u
(training/Adam/beta_2/Read/ReadVariableOpReadVariableOptraining/Adam/beta_2*
_output_shapes
: *
dtype0
|
training/Adam/beta_1VarHandleOp*
_output_shapes
: *
dtype0*
shape: *%
shared_nametraining/Adam/beta_1
u
(training/Adam/beta_1/Read/ReadVariableOpReadVariableOptraining/Adam/beta_1*
_output_shapes
: *
dtype0
x
training/Adam/iterVarHandleOp*
_output_shapes
: *
dtype0	*
shape: *#
shared_nametraining/Adam/iter
q
&training/Adam/iter/Read/ReadVariableOpReadVariableOptraining/Adam/iter*
_output_shapes
: *
dtype0	
p
dense_5/biasVarHandleOp*
_output_shapes
: *
dtype0*
shape:y*
shared_namedense_5/bias
i
 dense_5/bias/Read/ReadVariableOpReadVariableOpdense_5/bias*
_output_shapes
:y*
dtype0
x
dense_5/kernelVarHandleOp*
_output_shapes
: *
dtype0*
shape
:9y*
shared_namedense_5/kernel
q
"dense_5/kernel/Read/ReadVariableOpReadVariableOpdense_5/kernel*
_output_shapes

:9y*
dtype0
p
dense_4/biasVarHandleOp*
_output_shapes
: *
dtype0*
shape:9*
shared_namedense_4/bias
i
 dense_4/bias/Read/ReadVariableOpReadVariableOpdense_4/bias*
_output_shapes
:9*
dtype0
x
dense_4/kernelVarHandleOp*
_output_shapes
: *
dtype0*
shape
:F9*
shared_namedense_4/kernel
q
"dense_4/kernel/Read/ReadVariableOpReadVariableOpdense_4/kernel*
_output_shapes

:F9*
dtype0
p
dense_3/biasVarHandleOp*
_output_shapes
: *
dtype0*
shape:F*
shared_namedense_3/bias
i
 dense_3/bias/Read/ReadVariableOpReadVariableOpdense_3/bias*
_output_shapes
:F*
dtype0
x
dense_3/kernelVarHandleOp*
_output_shapes
: *
dtype0*
shape
:RF*
shared_namedense_3/kernel
q
"dense_3/kernel/Read/ReadVariableOpReadVariableOpdense_3/kernel*
_output_shapes

:RF*
dtype0
�
serving_default_dense_3_inputPlaceholder*'
_output_shapes
:���������R*
dtype0*
shape:���������R
�
StatefulPartitionedCallStatefulPartitionedCallserving_default_dense_3_inputdense_3/kerneldense_3/biasdense_4/kerneldense_4/biasdense_5/kerneldense_5/bias*
Tin
	2*
Tout
2*
_collective_manager_ids
 *'
_output_shapes
:���������y*(
_read_only_resource_inputs

*0
config_proto 

CPU

GPU2*0J 8� *.
f)R'
%__inference_signature_wrapper_1619390

NoOpNoOp
�5
ConstConst"/device:CPU:0*
_output_shapes
: *
dtype0*�5
value�5B�5 B�5
�
layer_with_weights-0
layer-0
layer-1
layer_with_weights-1
layer-2
layer-3
layer_with_weights-2
layer-4
	variables
trainable_variables
regularization_losses
		keras_api

__call__
*&call_and_return_all_conditional_losses
_default_save_signature
	optimizer

signatures*
�
	variables
trainable_variables
regularization_losses
	keras_api
__call__
*&call_and_return_all_conditional_losses

kernel
bias*
�
	variables
trainable_variables
regularization_losses
	keras_api
__call__
*&call_and_return_all_conditional_losses* 
�
	variables
trainable_variables
regularization_losses
 	keras_api
!__call__
*"&call_and_return_all_conditional_losses

#kernel
$bias*
�
%	variables
&trainable_variables
'regularization_losses
(	keras_api
)__call__
**&call_and_return_all_conditional_losses* 
�
+	variables
,trainable_variables
-regularization_losses
.	keras_api
/__call__
*0&call_and_return_all_conditional_losses

1kernel
2bias*
.
0
1
#2
$3
14
25*
.
0
1
#2
$3
14
25*
* 
�
3non_trainable_variables

4layers
5metrics
6layer_regularization_losses
7layer_metrics
	variables
trainable_variables
regularization_losses

__call__
_default_save_signature
*&call_and_return_all_conditional_losses
&"call_and_return_conditional_losses*

8trace_0
9trace_1* 
6
:trace_0
;trace_1
<trace_2
=trace_3* 
* 
�
>iter

?beta_1

@beta_2
	Adecay
Blearning_ratemmmn#mo$mp1mq2mrvsvt#vu$vv1vw2vx*

Cserving_default* 

0
1*

0
1*
* 
�
Dnon_trainable_variables

Elayers
Fmetrics
Glayer_regularization_losses
Hlayer_metrics
	variables
trainable_variables
regularization_losses
__call__
*&call_and_return_all_conditional_losses
&"call_and_return_conditional_losses*

Itrace_0* 

Jtrace_0* 
^X
VARIABLE_VALUEdense_3/kernel6layer_with_weights-0/kernel/.ATTRIBUTES/VARIABLE_VALUE*
ZT
VARIABLE_VALUEdense_3/bias4layer_with_weights-0/bias/.ATTRIBUTES/VARIABLE_VALUE*
* 
* 
* 
�
Knon_trainable_variables

Llayers
Mmetrics
Nlayer_regularization_losses
Olayer_metrics
	variables
trainable_variables
regularization_losses
__call__
*&call_and_return_all_conditional_losses
&"call_and_return_conditional_losses* 

Ptrace_0* 

Qtrace_0* 

#0
$1*

#0
$1*
* 
�
Rnon_trainable_variables

Slayers
Tmetrics
Ulayer_regularization_losses
Vlayer_metrics
	variables
trainable_variables
regularization_losses
!__call__
*"&call_and_return_all_conditional_losses
&""call_and_return_conditional_losses*

Wtrace_0* 

Xtrace_0* 
^X
VARIABLE_VALUEdense_4/kernel6layer_with_weights-1/kernel/.ATTRIBUTES/VARIABLE_VALUE*
ZT
VARIABLE_VALUEdense_4/bias4layer_with_weights-1/bias/.ATTRIBUTES/VARIABLE_VALUE*
* 
* 
* 
�
Ynon_trainable_variables

Zlayers
[metrics
\layer_regularization_losses
]layer_metrics
%	variables
&trainable_variables
'regularization_losses
)__call__
**&call_and_return_all_conditional_losses
&*"call_and_return_conditional_losses* 

^trace_0* 

_trace_0* 

10
21*

10
21*
* 
�
`non_trainable_variables

alayers
bmetrics
clayer_regularization_losses
dlayer_metrics
+	variables
,trainable_variables
-regularization_losses
/__call__
*0&call_and_return_all_conditional_losses
&0"call_and_return_conditional_losses*

etrace_0* 

ftrace_0* 
^X
VARIABLE_VALUEdense_5/kernel6layer_with_weights-2/kernel/.ATTRIBUTES/VARIABLE_VALUE*
ZT
VARIABLE_VALUEdense_5/bias4layer_with_weights-2/bias/.ATTRIBUTES/VARIABLE_VALUE*
* 
'
0
1
2
3
4*

g0*
* 
* 
* 
* 
* 
* 
* 
* 
UO
VARIABLE_VALUEtraining/Adam/iter)optimizer/iter/.ATTRIBUTES/VARIABLE_VALUE*
YS
VARIABLE_VALUEtraining/Adam/beta_1+optimizer/beta_1/.ATTRIBUTES/VARIABLE_VALUE*
YS
VARIABLE_VALUEtraining/Adam/beta_2+optimizer/beta_2/.ATTRIBUTES/VARIABLE_VALUE*
WQ
VARIABLE_VALUEtraining/Adam/decay*optimizer/decay/.ATTRIBUTES/VARIABLE_VALUE*
ga
VARIABLE_VALUEtraining/Adam/learning_rate2optimizer/learning_rate/.ATTRIBUTES/VARIABLE_VALUE*
* 
* 
* 
* 
* 
* 
* 
* 
* 
* 
* 
* 
* 
* 
* 
* 
* 
* 
* 
* 
* 
* 
* 
* 
* 
* 
* 
* 
* 
* 
* 
* 
* 
* 
* 
* 
H
h	variables
i	keras_api
	jtotal
	kcount
l
_fn_kwargs*

j0
k1*

h	variables*
UO
VARIABLE_VALUEtotal_14keras_api/metrics/0/total/.ATTRIBUTES/VARIABLE_VALUE*
UO
VARIABLE_VALUEcount_14keras_api/metrics/0/count/.ATTRIBUTES/VARIABLE_VALUE*
* 
��
VARIABLE_VALUEtraining/Adam/dense_3/kernel/mRlayer_with_weights-0/kernel/.OPTIMIZER_SLOT/optimizer/m/.ATTRIBUTES/VARIABLE_VALUE*
��
VARIABLE_VALUEtraining/Adam/dense_3/bias/mPlayer_with_weights-0/bias/.OPTIMIZER_SLOT/optimizer/m/.ATTRIBUTES/VARIABLE_VALUE*
��
VARIABLE_VALUEtraining/Adam/dense_4/kernel/mRlayer_with_weights-1/kernel/.OPTIMIZER_SLOT/optimizer/m/.ATTRIBUTES/VARIABLE_VALUE*
��
VARIABLE_VALUEtraining/Adam/dense_4/bias/mPlayer_with_weights-1/bias/.OPTIMIZER_SLOT/optimizer/m/.ATTRIBUTES/VARIABLE_VALUE*
��
VARIABLE_VALUEtraining/Adam/dense_5/kernel/mRlayer_with_weights-2/kernel/.OPTIMIZER_SLOT/optimizer/m/.ATTRIBUTES/VARIABLE_VALUE*
��
VARIABLE_VALUEtraining/Adam/dense_5/bias/mPlayer_with_weights-2/bias/.OPTIMIZER_SLOT/optimizer/m/.ATTRIBUTES/VARIABLE_VALUE*
��
VARIABLE_VALUEtraining/Adam/dense_3/kernel/vRlayer_with_weights-0/kernel/.OPTIMIZER_SLOT/optimizer/v/.ATTRIBUTES/VARIABLE_VALUE*
��
VARIABLE_VALUEtraining/Adam/dense_3/bias/vPlayer_with_weights-0/bias/.OPTIMIZER_SLOT/optimizer/v/.ATTRIBUTES/VARIABLE_VALUE*
��
VARIABLE_VALUEtraining/Adam/dense_4/kernel/vRlayer_with_weights-1/kernel/.OPTIMIZER_SLOT/optimizer/v/.ATTRIBUTES/VARIABLE_VALUE*
��
VARIABLE_VALUEtraining/Adam/dense_4/bias/vPlayer_with_weights-1/bias/.OPTIMIZER_SLOT/optimizer/v/.ATTRIBUTES/VARIABLE_VALUE*
��
VARIABLE_VALUEtraining/Adam/dense_5/kernel/vRlayer_with_weights-2/kernel/.OPTIMIZER_SLOT/optimizer/v/.ATTRIBUTES/VARIABLE_VALUE*
��
VARIABLE_VALUEtraining/Adam/dense_5/bias/vPlayer_with_weights-2/bias/.OPTIMIZER_SLOT/optimizer/v/.ATTRIBUTES/VARIABLE_VALUE*
O
saver_filenamePlaceholder*
_output_shapes
: *
dtype0*
shape: 
�
StatefulPartitionedCall_1StatefulPartitionedCallsaver_filenamedense_3/kerneldense_3/biasdense_4/kerneldense_4/biasdense_5/kerneldense_5/biastraining/Adam/itertraining/Adam/beta_1training/Adam/beta_2training/Adam/decaytraining/Adam/learning_ratetotal_1count_1training/Adam/dense_3/kernel/mtraining/Adam/dense_3/bias/mtraining/Adam/dense_4/kernel/mtraining/Adam/dense_4/bias/mtraining/Adam/dense_5/kernel/mtraining/Adam/dense_5/bias/mtraining/Adam/dense_3/kernel/vtraining/Adam/dense_3/bias/vtraining/Adam/dense_4/kernel/vtraining/Adam/dense_4/bias/vtraining/Adam/dense_5/kernel/vtraining/Adam/dense_5/bias/vConst*&
Tin
2*
Tout
2*
_collective_manager_ids
 *
_output_shapes
: * 
_read_only_resource_inputs
 *0
config_proto 

CPU

GPU2*0J 8� *)
f$R"
 __inference__traced_save_1619681
�
StatefulPartitionedCall_2StatefulPartitionedCallsaver_filenamedense_3/kerneldense_3/biasdense_4/kerneldense_4/biasdense_5/kerneldense_5/biastraining/Adam/itertraining/Adam/beta_1training/Adam/beta_2training/Adam/decaytraining/Adam/learning_ratetotal_1count_1training/Adam/dense_3/kernel/mtraining/Adam/dense_3/bias/mtraining/Adam/dense_4/kernel/mtraining/Adam/dense_4/bias/mtraining/Adam/dense_5/kernel/mtraining/Adam/dense_5/bias/mtraining/Adam/dense_3/kernel/vtraining/Adam/dense_3/bias/vtraining/Adam/dense_4/kernel/vtraining/Adam/dense_4/bias/vtraining/Adam/dense_5/kernel/vtraining/Adam/dense_5/bias/v*%
Tin
2*
Tout
2*
_collective_manager_ids
 *
_output_shapes
: * 
_read_only_resource_inputs
 *0
config_proto 

CPU

GPU2*0J 8� *,
f'R%
#__inference__traced_restore_1619765�
�
K
/__inference_leaky_re_lu_3_layer_call_fn_1619487

inputs
identity�
PartitionedCallPartitionedCallinputs*
Tin
2*
Tout
2*
_collective_manager_ids
 *'
_output_shapes
:���������9* 
_read_only_resource_inputs
 *0
config_proto 

CPU

GPU2*0J 8� *S
fNRL
J__inference_leaky_re_lu_3_layer_call_and_return_conditional_losses_1619224`
IdentityIdentityPartitionedCall:output:0*
T0*'
_output_shapes
:���������9"
identityIdentity:output:0*(
_construction_contextkEagerRuntime*&
_input_shapes
:���������9:O K
'
_output_shapes
:���������9
 
_user_specified_nameinputs
�
f
J__inference_leaky_re_lu_2_layer_call_and_return_conditional_losses_1619205

inputs
identityW
	LeakyRelu	LeakyReluinputs*'
_output_shapes
:���������F*
alpha%���>_
IdentityIdentityLeakyRelu:activations:0*
T0*'
_output_shapes
:���������F"
identityIdentity:output:0*(
_construction_contextkEagerRuntime*&
_input_shapes
:���������F:O K
'
_output_shapes
:���������F
 
_user_specified_nameinputs
�
�
.__inference_sequential_1_layer_call_fn_1619307
dense_3_input 
dense_3_kernel:RF
dense_3_bias:F 
dense_4_kernel:F9
dense_4_bias:9 
dense_5_kernel:9y
dense_5_bias:y
identity��StatefulPartitionedCall�
StatefulPartitionedCallStatefulPartitionedCalldense_3_inputdense_3_kerneldense_3_biasdense_4_kerneldense_4_biasdense_5_kerneldense_5_bias*
Tin
	2*
Tout
2*
_collective_manager_ids
 *'
_output_shapes
:���������y*(
_read_only_resource_inputs

*0
config_proto 

CPU

GPU2*0J 8� *R
fMRK
I__inference_sequential_1_layer_call_and_return_conditional_losses_1619298o
IdentityIdentity StatefulPartitionedCall:output:0^NoOp*
T0*'
_output_shapes
:���������y<
NoOpNoOp^StatefulPartitionedCall*
_output_shapes
 "
identityIdentity:output:0*(
_construction_contextkEagerRuntime*2
_input_shapes!
:���������R: : : : : : 22
StatefulPartitionedCallStatefulPartitionedCall:,(
&
_user_specified_namedense_5/bias:.*
(
_user_specified_namedense_5/kernel:,(
&
_user_specified_namedense_4/bias:.*
(
_user_specified_namedense_4/kernel:,(
&
_user_specified_namedense_3/bias:.*
(
_user_specified_namedense_3/kernel:V R
'
_output_shapes
:���������R
'
_user_specified_namedense_3_input
�
�
%__inference_signature_wrapper_1619390
dense_3_input 
dense_3_kernel:RF
dense_3_bias:F 
dense_4_kernel:F9
dense_4_bias:9 
dense_5_kernel:9y
dense_5_bias:y
identity��StatefulPartitionedCall�
StatefulPartitionedCallStatefulPartitionedCalldense_3_inputdense_3_kerneldense_3_biasdense_4_kerneldense_4_biasdense_5_kerneldense_5_bias*
Tin
	2*
Tout
2*
_collective_manager_ids
 *'
_output_shapes
:���������y*(
_read_only_resource_inputs

*0
config_proto 

CPU

GPU2*0J 8� *+
f&R$
"__inference__wrapped_model_1619185o
IdentityIdentity StatefulPartitionedCall:output:0^NoOp*
T0*'
_output_shapes
:���������y<
NoOpNoOp^StatefulPartitionedCall*
_output_shapes
 "
identityIdentity:output:0*(
_construction_contextkEagerRuntime*2
_input_shapes!
:���������R: : : : : : 22
StatefulPartitionedCallStatefulPartitionedCall:,(
&
_user_specified_namedense_5/bias:.*
(
_user_specified_namedense_5/kernel:,(
&
_user_specified_namedense_4/bias:.*
(
_user_specified_namedense_4/kernel:,(
&
_user_specified_namedense_3/bias:.*
(
_user_specified_namedense_3/kernel:V R
'
_output_shapes
:���������R
'
_user_specified_namedense_3_input
�
�
I__inference_sequential_1_layer_call_and_return_conditional_losses_1619438

inputs>
,dense_3_matmul_readvariableop_dense_3_kernel:RF9
+dense_3_biasadd_readvariableop_dense_3_bias:F>
,dense_4_matmul_readvariableop_dense_4_kernel:F99
+dense_4_biasadd_readvariableop_dense_4_bias:9>
,dense_5_matmul_readvariableop_dense_5_kernel:9y9
+dense_5_biasadd_readvariableop_dense_5_bias:y
identity��dense_3/BiasAdd/ReadVariableOp�dense_3/MatMul/ReadVariableOp�dense_4/BiasAdd/ReadVariableOp�dense_4/MatMul/ReadVariableOp�dense_5/BiasAdd/ReadVariableOp�dense_5/MatMul/ReadVariableOp�
dense_3/MatMul/ReadVariableOpReadVariableOp,dense_3_matmul_readvariableop_dense_3_kernel*
_output_shapes

:RF*
dtype0y
dense_3/MatMulMatMulinputs%dense_3/MatMul/ReadVariableOp:value:0*
T0*'
_output_shapes
:���������F�
dense_3/BiasAdd/ReadVariableOpReadVariableOp+dense_3_biasadd_readvariableop_dense_3_bias*
_output_shapes
:F*
dtype0�
dense_3/BiasAddBiasAdddense_3/MatMul:product:0&dense_3/BiasAdd/ReadVariableOp:value:0*
T0*'
_output_shapes
:���������Fw
leaky_re_lu_2/LeakyRelu	LeakyReludense_3/BiasAdd:output:0*'
_output_shapes
:���������F*
alpha%���>�
dense_4/MatMul/ReadVariableOpReadVariableOp,dense_4_matmul_readvariableop_dense_4_kernel*
_output_shapes

:F9*
dtype0�
dense_4/MatMulMatMul%leaky_re_lu_2/LeakyRelu:activations:0%dense_4/MatMul/ReadVariableOp:value:0*
T0*'
_output_shapes
:���������9�
dense_4/BiasAdd/ReadVariableOpReadVariableOp+dense_4_biasadd_readvariableop_dense_4_bias*
_output_shapes
:9*
dtype0�
dense_4/BiasAddBiasAdddense_4/MatMul:product:0&dense_4/BiasAdd/ReadVariableOp:value:0*
T0*'
_output_shapes
:���������9w
leaky_re_lu_3/LeakyRelu	LeakyReludense_4/BiasAdd:output:0*'
_output_shapes
:���������9*
alpha%���>�
dense_5/MatMul/ReadVariableOpReadVariableOp,dense_5_matmul_readvariableop_dense_5_kernel*
_output_shapes

:9y*
dtype0�
dense_5/MatMulMatMul%leaky_re_lu_3/LeakyRelu:activations:0%dense_5/MatMul/ReadVariableOp:value:0*
T0*'
_output_shapes
:���������y�
dense_5/BiasAdd/ReadVariableOpReadVariableOp+dense_5_biasadd_readvariableop_dense_5_bias*
_output_shapes
:y*
dtype0�
dense_5/BiasAddBiasAdddense_5/MatMul:product:0&dense_5/BiasAdd/ReadVariableOp:value:0*
T0*'
_output_shapes
:���������yg
IdentityIdentitydense_5/BiasAdd:output:0^NoOp*
T0*'
_output_shapes
:���������y�
NoOpNoOp^dense_3/BiasAdd/ReadVariableOp^dense_3/MatMul/ReadVariableOp^dense_4/BiasAdd/ReadVariableOp^dense_4/MatMul/ReadVariableOp^dense_5/BiasAdd/ReadVariableOp^dense_5/MatMul/ReadVariableOp*
_output_shapes
 "
identityIdentity:output:0*(
_construction_contextkEagerRuntime*2
_input_shapes!
:���������R: : : : : : 2@
dense_3/BiasAdd/ReadVariableOpdense_3/BiasAdd/ReadVariableOp2>
dense_3/MatMul/ReadVariableOpdense_3/MatMul/ReadVariableOp2@
dense_4/BiasAdd/ReadVariableOpdense_4/BiasAdd/ReadVariableOp2>
dense_4/MatMul/ReadVariableOpdense_4/MatMul/ReadVariableOp2@
dense_5/BiasAdd/ReadVariableOpdense_5/BiasAdd/ReadVariableOp2>
dense_5/MatMul/ReadVariableOpdense_5/MatMul/ReadVariableOp:,(
&
_user_specified_namedense_5/bias:.*
(
_user_specified_namedense_5/kernel:,(
&
_user_specified_namedense_4/bias:.*
(
_user_specified_namedense_4/kernel:,(
&
_user_specified_namedense_3/bias:.*
(
_user_specified_namedense_3/kernel:O K
'
_output_shapes
:���������R
 
_user_specified_nameinputs
��
�
 __inference__traced_save_1619681
file_prefix7
%read_disablecopyonread_dense_3_kernel:RF3
%read_1_disablecopyonread_dense_3_bias:F9
'read_2_disablecopyonread_dense_4_kernel:F93
%read_3_disablecopyonread_dense_4_bias:99
'read_4_disablecopyonread_dense_5_kernel:9y3
%read_5_disablecopyonread_dense_5_bias:y5
+read_6_disablecopyonread_training_adam_iter:	 7
-read_7_disablecopyonread_training_adam_beta_1: 7
-read_8_disablecopyonread_training_adam_beta_2: 6
,read_9_disablecopyonread_training_adam_decay: ?
5read_10_disablecopyonread_training_adam_learning_rate: +
!read_11_disablecopyonread_total_1: +
!read_12_disablecopyonread_count_1: J
8read_13_disablecopyonread_training_adam_dense_3_kernel_m:RFD
6read_14_disablecopyonread_training_adam_dense_3_bias_m:FJ
8read_15_disablecopyonread_training_adam_dense_4_kernel_m:F9D
6read_16_disablecopyonread_training_adam_dense_4_bias_m:9J
8read_17_disablecopyonread_training_adam_dense_5_kernel_m:9yD
6read_18_disablecopyonread_training_adam_dense_5_bias_m:yJ
8read_19_disablecopyonread_training_adam_dense_3_kernel_v:RFD
6read_20_disablecopyonread_training_adam_dense_3_bias_v:FJ
8read_21_disablecopyonread_training_adam_dense_4_kernel_v:F9D
6read_22_disablecopyonread_training_adam_dense_4_bias_v:9J
8read_23_disablecopyonread_training_adam_dense_5_kernel_v:9yD
6read_24_disablecopyonread_training_adam_dense_5_bias_v:y
savev2_const
identity_51��MergeV2Checkpoints�Read/DisableCopyOnRead�Read/ReadVariableOp�Read_1/DisableCopyOnRead�Read_1/ReadVariableOp�Read_10/DisableCopyOnRead�Read_10/ReadVariableOp�Read_11/DisableCopyOnRead�Read_11/ReadVariableOp�Read_12/DisableCopyOnRead�Read_12/ReadVariableOp�Read_13/DisableCopyOnRead�Read_13/ReadVariableOp�Read_14/DisableCopyOnRead�Read_14/ReadVariableOp�Read_15/DisableCopyOnRead�Read_15/ReadVariableOp�Read_16/DisableCopyOnRead�Read_16/ReadVariableOp�Read_17/DisableCopyOnRead�Read_17/ReadVariableOp�Read_18/DisableCopyOnRead�Read_18/ReadVariableOp�Read_19/DisableCopyOnRead�Read_19/ReadVariableOp�Read_2/DisableCopyOnRead�Read_2/ReadVariableOp�Read_20/DisableCopyOnRead�Read_20/ReadVariableOp�Read_21/DisableCopyOnRead�Read_21/ReadVariableOp�Read_22/DisableCopyOnRead�Read_22/ReadVariableOp�Read_23/DisableCopyOnRead�Read_23/ReadVariableOp�Read_24/DisableCopyOnRead�Read_24/ReadVariableOp�Read_3/DisableCopyOnRead�Read_3/ReadVariableOp�Read_4/DisableCopyOnRead�Read_4/ReadVariableOp�Read_5/DisableCopyOnRead�Read_5/ReadVariableOp�Read_6/DisableCopyOnRead�Read_6/ReadVariableOp�Read_7/DisableCopyOnRead�Read_7/ReadVariableOp�Read_8/DisableCopyOnRead�Read_8/ReadVariableOp�Read_9/DisableCopyOnRead�Read_9/ReadVariableOpw
StaticRegexFullMatchStaticRegexFullMatchfile_prefix"/device:CPU:**
_output_shapes
: *
pattern
^s3://.*Z
ConstConst"/device:CPU:**
_output_shapes
: *
dtype0*
valueB B.parta
Const_1Const"/device:CPU:**
_output_shapes
: *
dtype0*
valueB B
_temp/part�
SelectSelectStaticRegexFullMatch:output:0Const:output:0Const_1:output:0"/device:CPU:**
T0*
_output_shapes
: f

StringJoin
StringJoinfile_prefixSelect:output:0"/device:CPU:**
N*
_output_shapes
: L

num_shardsConst*
_output_shapes
: *
dtype0*
value	B :f
ShardedFilename/shardConst"/device:CPU:0*
_output_shapes
: *
dtype0*
value	B : �
ShardedFilenameShardedFilenameStringJoin:output:0ShardedFilename/shard:output:0num_shards:output:0"/device:CPU:0*
_output_shapes
: w
Read/DisableCopyOnReadDisableCopyOnRead%read_disablecopyonread_dense_3_kernel"/device:CPU:0*
_output_shapes
 �
Read/ReadVariableOpReadVariableOp%read_disablecopyonread_dense_3_kernel^Read/DisableCopyOnRead"/device:CPU:0*
_output_shapes

:RF*
dtype0i
IdentityIdentityRead/ReadVariableOp:value:0"/device:CPU:0*
T0*
_output_shapes

:RFa

Identity_1IdentityIdentity:output:0"/device:CPU:0*
T0*
_output_shapes

:RFy
Read_1/DisableCopyOnReadDisableCopyOnRead%read_1_disablecopyonread_dense_3_bias"/device:CPU:0*
_output_shapes
 �
Read_1/ReadVariableOpReadVariableOp%read_1_disablecopyonread_dense_3_bias^Read_1/DisableCopyOnRead"/device:CPU:0*
_output_shapes
:F*
dtype0i

Identity_2IdentityRead_1/ReadVariableOp:value:0"/device:CPU:0*
T0*
_output_shapes
:F_

Identity_3IdentityIdentity_2:output:0"/device:CPU:0*
T0*
_output_shapes
:F{
Read_2/DisableCopyOnReadDisableCopyOnRead'read_2_disablecopyonread_dense_4_kernel"/device:CPU:0*
_output_shapes
 �
Read_2/ReadVariableOpReadVariableOp'read_2_disablecopyonread_dense_4_kernel^Read_2/DisableCopyOnRead"/device:CPU:0*
_output_shapes

:F9*
dtype0m

Identity_4IdentityRead_2/ReadVariableOp:value:0"/device:CPU:0*
T0*
_output_shapes

:F9c

Identity_5IdentityIdentity_4:output:0"/device:CPU:0*
T0*
_output_shapes

:F9y
Read_3/DisableCopyOnReadDisableCopyOnRead%read_3_disablecopyonread_dense_4_bias"/device:CPU:0*
_output_shapes
 �
Read_3/ReadVariableOpReadVariableOp%read_3_disablecopyonread_dense_4_bias^Read_3/DisableCopyOnRead"/device:CPU:0*
_output_shapes
:9*
dtype0i

Identity_6IdentityRead_3/ReadVariableOp:value:0"/device:CPU:0*
T0*
_output_shapes
:9_

Identity_7IdentityIdentity_6:output:0"/device:CPU:0*
T0*
_output_shapes
:9{
Read_4/DisableCopyOnReadDisableCopyOnRead'read_4_disablecopyonread_dense_5_kernel"/device:CPU:0*
_output_shapes
 �
Read_4/ReadVariableOpReadVariableOp'read_4_disablecopyonread_dense_5_kernel^Read_4/DisableCopyOnRead"/device:CPU:0*
_output_shapes

:9y*
dtype0m

Identity_8IdentityRead_4/ReadVariableOp:value:0"/device:CPU:0*
T0*
_output_shapes

:9yc

Identity_9IdentityIdentity_8:output:0"/device:CPU:0*
T0*
_output_shapes

:9yy
Read_5/DisableCopyOnReadDisableCopyOnRead%read_5_disablecopyonread_dense_5_bias"/device:CPU:0*
_output_shapes
 �
Read_5/ReadVariableOpReadVariableOp%read_5_disablecopyonread_dense_5_bias^Read_5/DisableCopyOnRead"/device:CPU:0*
_output_shapes
:y*
dtype0j
Identity_10IdentityRead_5/ReadVariableOp:value:0"/device:CPU:0*
T0*
_output_shapes
:ya
Identity_11IdentityIdentity_10:output:0"/device:CPU:0*
T0*
_output_shapes
:y
Read_6/DisableCopyOnReadDisableCopyOnRead+read_6_disablecopyonread_training_adam_iter"/device:CPU:0*
_output_shapes
 �
Read_6/ReadVariableOpReadVariableOp+read_6_disablecopyonread_training_adam_iter^Read_6/DisableCopyOnRead"/device:CPU:0*
_output_shapes
: *
dtype0	f
Identity_12IdentityRead_6/ReadVariableOp:value:0"/device:CPU:0*
T0	*
_output_shapes
: ]
Identity_13IdentityIdentity_12:output:0"/device:CPU:0*
T0	*
_output_shapes
: �
Read_7/DisableCopyOnReadDisableCopyOnRead-read_7_disablecopyonread_training_adam_beta_1"/device:CPU:0*
_output_shapes
 �
Read_7/ReadVariableOpReadVariableOp-read_7_disablecopyonread_training_adam_beta_1^Read_7/DisableCopyOnRead"/device:CPU:0*
_output_shapes
: *
dtype0f
Identity_14IdentityRead_7/ReadVariableOp:value:0"/device:CPU:0*
T0*
_output_shapes
: ]
Identity_15IdentityIdentity_14:output:0"/device:CPU:0*
T0*
_output_shapes
: �
Read_8/DisableCopyOnReadDisableCopyOnRead-read_8_disablecopyonread_training_adam_beta_2"/device:CPU:0*
_output_shapes
 �
Read_8/ReadVariableOpReadVariableOp-read_8_disablecopyonread_training_adam_beta_2^Read_8/DisableCopyOnRead"/device:CPU:0*
_output_shapes
: *
dtype0f
Identity_16IdentityRead_8/ReadVariableOp:value:0"/device:CPU:0*
T0*
_output_shapes
: ]
Identity_17IdentityIdentity_16:output:0"/device:CPU:0*
T0*
_output_shapes
: �
Read_9/DisableCopyOnReadDisableCopyOnRead,read_9_disablecopyonread_training_adam_decay"/device:CPU:0*
_output_shapes
 �
Read_9/ReadVariableOpReadVariableOp,read_9_disablecopyonread_training_adam_decay^Read_9/DisableCopyOnRead"/device:CPU:0*
_output_shapes
: *
dtype0f
Identity_18IdentityRead_9/ReadVariableOp:value:0"/device:CPU:0*
T0*
_output_shapes
: ]
Identity_19IdentityIdentity_18:output:0"/device:CPU:0*
T0*
_output_shapes
: �
Read_10/DisableCopyOnReadDisableCopyOnRead5read_10_disablecopyonread_training_adam_learning_rate"/device:CPU:0*
_output_shapes
 �
Read_10/ReadVariableOpReadVariableOp5read_10_disablecopyonread_training_adam_learning_rate^Read_10/DisableCopyOnRead"/device:CPU:0*
_output_shapes
: *
dtype0g
Identity_20IdentityRead_10/ReadVariableOp:value:0"/device:CPU:0*
T0*
_output_shapes
: ]
Identity_21IdentityIdentity_20:output:0"/device:CPU:0*
T0*
_output_shapes
: v
Read_11/DisableCopyOnReadDisableCopyOnRead!read_11_disablecopyonread_total_1"/device:CPU:0*
_output_shapes
 �
Read_11/ReadVariableOpReadVariableOp!read_11_disablecopyonread_total_1^Read_11/DisableCopyOnRead"/device:CPU:0*
_output_shapes
: *
dtype0g
Identity_22IdentityRead_11/ReadVariableOp:value:0"/device:CPU:0*
T0*
_output_shapes
: ]
Identity_23IdentityIdentity_22:output:0"/device:CPU:0*
T0*
_output_shapes
: v
Read_12/DisableCopyOnReadDisableCopyOnRead!read_12_disablecopyonread_count_1"/device:CPU:0*
_output_shapes
 �
Read_12/ReadVariableOpReadVariableOp!read_12_disablecopyonread_count_1^Read_12/DisableCopyOnRead"/device:CPU:0*
_output_shapes
: *
dtype0g
Identity_24IdentityRead_12/ReadVariableOp:value:0"/device:CPU:0*
T0*
_output_shapes
: ]
Identity_25IdentityIdentity_24:output:0"/device:CPU:0*
T0*
_output_shapes
: �
Read_13/DisableCopyOnReadDisableCopyOnRead8read_13_disablecopyonread_training_adam_dense_3_kernel_m"/device:CPU:0*
_output_shapes
 �
Read_13/ReadVariableOpReadVariableOp8read_13_disablecopyonread_training_adam_dense_3_kernel_m^Read_13/DisableCopyOnRead"/device:CPU:0*
_output_shapes

:RF*
dtype0o
Identity_26IdentityRead_13/ReadVariableOp:value:0"/device:CPU:0*
T0*
_output_shapes

:RFe
Identity_27IdentityIdentity_26:output:0"/device:CPU:0*
T0*
_output_shapes

:RF�
Read_14/DisableCopyOnReadDisableCopyOnRead6read_14_disablecopyonread_training_adam_dense_3_bias_m"/device:CPU:0*
_output_shapes
 �
Read_14/ReadVariableOpReadVariableOp6read_14_disablecopyonread_training_adam_dense_3_bias_m^Read_14/DisableCopyOnRead"/device:CPU:0*
_output_shapes
:F*
dtype0k
Identity_28IdentityRead_14/ReadVariableOp:value:0"/device:CPU:0*
T0*
_output_shapes
:Fa
Identity_29IdentityIdentity_28:output:0"/device:CPU:0*
T0*
_output_shapes
:F�
Read_15/DisableCopyOnReadDisableCopyOnRead8read_15_disablecopyonread_training_adam_dense_4_kernel_m"/device:CPU:0*
_output_shapes
 �
Read_15/ReadVariableOpReadVariableOp8read_15_disablecopyonread_training_adam_dense_4_kernel_m^Read_15/DisableCopyOnRead"/device:CPU:0*
_output_shapes

:F9*
dtype0o
Identity_30IdentityRead_15/ReadVariableOp:value:0"/device:CPU:0*
T0*
_output_shapes

:F9e
Identity_31IdentityIdentity_30:output:0"/device:CPU:0*
T0*
_output_shapes

:F9�
Read_16/DisableCopyOnReadDisableCopyOnRead6read_16_disablecopyonread_training_adam_dense_4_bias_m"/device:CPU:0*
_output_shapes
 �
Read_16/ReadVariableOpReadVariableOp6read_16_disablecopyonread_training_adam_dense_4_bias_m^Read_16/DisableCopyOnRead"/device:CPU:0*
_output_shapes
:9*
dtype0k
Identity_32IdentityRead_16/ReadVariableOp:value:0"/device:CPU:0*
T0*
_output_shapes
:9a
Identity_33IdentityIdentity_32:output:0"/device:CPU:0*
T0*
_output_shapes
:9�
Read_17/DisableCopyOnReadDisableCopyOnRead8read_17_disablecopyonread_training_adam_dense_5_kernel_m"/device:CPU:0*
_output_shapes
 �
Read_17/ReadVariableOpReadVariableOp8read_17_disablecopyonread_training_adam_dense_5_kernel_m^Read_17/DisableCopyOnRead"/device:CPU:0*
_output_shapes

:9y*
dtype0o
Identity_34IdentityRead_17/ReadVariableOp:value:0"/device:CPU:0*
T0*
_output_shapes

:9ye
Identity_35IdentityIdentity_34:output:0"/device:CPU:0*
T0*
_output_shapes

:9y�
Read_18/DisableCopyOnReadDisableCopyOnRead6read_18_disablecopyonread_training_adam_dense_5_bias_m"/device:CPU:0*
_output_shapes
 �
Read_18/ReadVariableOpReadVariableOp6read_18_disablecopyonread_training_adam_dense_5_bias_m^Read_18/DisableCopyOnRead"/device:CPU:0*
_output_shapes
:y*
dtype0k
Identity_36IdentityRead_18/ReadVariableOp:value:0"/device:CPU:0*
T0*
_output_shapes
:ya
Identity_37IdentityIdentity_36:output:0"/device:CPU:0*
T0*
_output_shapes
:y�
Read_19/DisableCopyOnReadDisableCopyOnRead8read_19_disablecopyonread_training_adam_dense_3_kernel_v"/device:CPU:0*
_output_shapes
 �
Read_19/ReadVariableOpReadVariableOp8read_19_disablecopyonread_training_adam_dense_3_kernel_v^Read_19/DisableCopyOnRead"/device:CPU:0*
_output_shapes

:RF*
dtype0o
Identity_38IdentityRead_19/ReadVariableOp:value:0"/device:CPU:0*
T0*
_output_shapes

:RFe
Identity_39IdentityIdentity_38:output:0"/device:CPU:0*
T0*
_output_shapes

:RF�
Read_20/DisableCopyOnReadDisableCopyOnRead6read_20_disablecopyonread_training_adam_dense_3_bias_v"/device:CPU:0*
_output_shapes
 �
Read_20/ReadVariableOpReadVariableOp6read_20_disablecopyonread_training_adam_dense_3_bias_v^Read_20/DisableCopyOnRead"/device:CPU:0*
_output_shapes
:F*
dtype0k
Identity_40IdentityRead_20/ReadVariableOp:value:0"/device:CPU:0*
T0*
_output_shapes
:Fa
Identity_41IdentityIdentity_40:output:0"/device:CPU:0*
T0*
_output_shapes
:F�
Read_21/DisableCopyOnReadDisableCopyOnRead8read_21_disablecopyonread_training_adam_dense_4_kernel_v"/device:CPU:0*
_output_shapes
 �
Read_21/ReadVariableOpReadVariableOp8read_21_disablecopyonread_training_adam_dense_4_kernel_v^Read_21/DisableCopyOnRead"/device:CPU:0*
_output_shapes

:F9*
dtype0o
Identity_42IdentityRead_21/ReadVariableOp:value:0"/device:CPU:0*
T0*
_output_shapes

:F9e
Identity_43IdentityIdentity_42:output:0"/device:CPU:0*
T0*
_output_shapes

:F9�
Read_22/DisableCopyOnReadDisableCopyOnRead6read_22_disablecopyonread_training_adam_dense_4_bias_v"/device:CPU:0*
_output_shapes
 �
Read_22/ReadVariableOpReadVariableOp6read_22_disablecopyonread_training_adam_dense_4_bias_v^Read_22/DisableCopyOnRead"/device:CPU:0*
_output_shapes
:9*
dtype0k
Identity_44IdentityRead_22/ReadVariableOp:value:0"/device:CPU:0*
T0*
_output_shapes
:9a
Identity_45IdentityIdentity_44:output:0"/device:CPU:0*
T0*
_output_shapes
:9�
Read_23/DisableCopyOnReadDisableCopyOnRead8read_23_disablecopyonread_training_adam_dense_5_kernel_v"/device:CPU:0*
_output_shapes
 �
Read_23/ReadVariableOpReadVariableOp8read_23_disablecopyonread_training_adam_dense_5_kernel_v^Read_23/DisableCopyOnRead"/device:CPU:0*
_output_shapes

:9y*
dtype0o
Identity_46IdentityRead_23/ReadVariableOp:value:0"/device:CPU:0*
T0*
_output_shapes

:9ye
Identity_47IdentityIdentity_46:output:0"/device:CPU:0*
T0*
_output_shapes

:9y�
Read_24/DisableCopyOnReadDisableCopyOnRead6read_24_disablecopyonread_training_adam_dense_5_bias_v"/device:CPU:0*
_output_shapes
 �
Read_24/ReadVariableOpReadVariableOp6read_24_disablecopyonread_training_adam_dense_5_bias_v^Read_24/DisableCopyOnRead"/device:CPU:0*
_output_shapes
:y*
dtype0k
Identity_48IdentityRead_24/ReadVariableOp:value:0"/device:CPU:0*
T0*
_output_shapes
:ya
Identity_49IdentityIdentity_48:output:0"/device:CPU:0*
T0*
_output_shapes
:y�
SaveV2/tensor_namesConst"/device:CPU:0*
_output_shapes
:*
dtype0*�
value�B�B6layer_with_weights-0/kernel/.ATTRIBUTES/VARIABLE_VALUEB4layer_with_weights-0/bias/.ATTRIBUTES/VARIABLE_VALUEB6layer_with_weights-1/kernel/.ATTRIBUTES/VARIABLE_VALUEB4layer_with_weights-1/bias/.ATTRIBUTES/VARIABLE_VALUEB6layer_with_weights-2/kernel/.ATTRIBUTES/VARIABLE_VALUEB4layer_with_weights-2/bias/.ATTRIBUTES/VARIABLE_VALUEB)optimizer/iter/.ATTRIBUTES/VARIABLE_VALUEB+optimizer/beta_1/.ATTRIBUTES/VARIABLE_VALUEB+optimizer/beta_2/.ATTRIBUTES/VARIABLE_VALUEB*optimizer/decay/.ATTRIBUTES/VARIABLE_VALUEB2optimizer/learning_rate/.ATTRIBUTES/VARIABLE_VALUEB4keras_api/metrics/0/total/.ATTRIBUTES/VARIABLE_VALUEB4keras_api/metrics/0/count/.ATTRIBUTES/VARIABLE_VALUEBRlayer_with_weights-0/kernel/.OPTIMIZER_SLOT/optimizer/m/.ATTRIBUTES/VARIABLE_VALUEBPlayer_with_weights-0/bias/.OPTIMIZER_SLOT/optimizer/m/.ATTRIBUTES/VARIABLE_VALUEBRlayer_with_weights-1/kernel/.OPTIMIZER_SLOT/optimizer/m/.ATTRIBUTES/VARIABLE_VALUEBPlayer_with_weights-1/bias/.OPTIMIZER_SLOT/optimizer/m/.ATTRIBUTES/VARIABLE_VALUEBRlayer_with_weights-2/kernel/.OPTIMIZER_SLOT/optimizer/m/.ATTRIBUTES/VARIABLE_VALUEBPlayer_with_weights-2/bias/.OPTIMIZER_SLOT/optimizer/m/.ATTRIBUTES/VARIABLE_VALUEBRlayer_with_weights-0/kernel/.OPTIMIZER_SLOT/optimizer/v/.ATTRIBUTES/VARIABLE_VALUEBPlayer_with_weights-0/bias/.OPTIMIZER_SLOT/optimizer/v/.ATTRIBUTES/VARIABLE_VALUEBRlayer_with_weights-1/kernel/.OPTIMIZER_SLOT/optimizer/v/.ATTRIBUTES/VARIABLE_VALUEBPlayer_with_weights-1/bias/.OPTIMIZER_SLOT/optimizer/v/.ATTRIBUTES/VARIABLE_VALUEBRlayer_with_weights-2/kernel/.OPTIMIZER_SLOT/optimizer/v/.ATTRIBUTES/VARIABLE_VALUEBPlayer_with_weights-2/bias/.OPTIMIZER_SLOT/optimizer/v/.ATTRIBUTES/VARIABLE_VALUEB_CHECKPOINTABLE_OBJECT_GRAPH�
SaveV2/shape_and_slicesConst"/device:CPU:0*
_output_shapes
:*
dtype0*G
value>B<B B B B B B B B B B B B B B B B B B B B B B B B B B �
SaveV2SaveV2ShardedFilename:filename:0SaveV2/tensor_names:output:0 SaveV2/shape_and_slices:output:0Identity_1:output:0Identity_3:output:0Identity_5:output:0Identity_7:output:0Identity_9:output:0Identity_11:output:0Identity_13:output:0Identity_15:output:0Identity_17:output:0Identity_19:output:0Identity_21:output:0Identity_23:output:0Identity_25:output:0Identity_27:output:0Identity_29:output:0Identity_31:output:0Identity_33:output:0Identity_35:output:0Identity_37:output:0Identity_39:output:0Identity_41:output:0Identity_43:output:0Identity_45:output:0Identity_47:output:0Identity_49:output:0savev2_const"/device:CPU:0*&
 _has_manual_control_dependencies(*
_output_shapes
 *(
dtypes
2	�
&MergeV2Checkpoints/checkpoint_prefixesPackShardedFilename:filename:0^SaveV2"/device:CPU:0*
N*
T0*
_output_shapes
:�
MergeV2CheckpointsMergeV2Checkpoints/MergeV2Checkpoints/checkpoint_prefixes:output:0file_prefix"/device:CPU:0*&
 _has_manual_control_dependencies(*
_output_shapes
 i
Identity_50Identityfile_prefix^MergeV2Checkpoints"/device:CPU:0*
T0*
_output_shapes
: U
Identity_51IdentityIdentity_50:output:0^NoOp*
T0*
_output_shapes
: �

NoOpNoOp^MergeV2Checkpoints^Read/DisableCopyOnRead^Read/ReadVariableOp^Read_1/DisableCopyOnRead^Read_1/ReadVariableOp^Read_10/DisableCopyOnRead^Read_10/ReadVariableOp^Read_11/DisableCopyOnRead^Read_11/ReadVariableOp^Read_12/DisableCopyOnRead^Read_12/ReadVariableOp^Read_13/DisableCopyOnRead^Read_13/ReadVariableOp^Read_14/DisableCopyOnRead^Read_14/ReadVariableOp^Read_15/DisableCopyOnRead^Read_15/ReadVariableOp^Read_16/DisableCopyOnRead^Read_16/ReadVariableOp^Read_17/DisableCopyOnRead^Read_17/ReadVariableOp^Read_18/DisableCopyOnRead^Read_18/ReadVariableOp^Read_19/DisableCopyOnRead^Read_19/ReadVariableOp^Read_2/DisableCopyOnRead^Read_2/ReadVariableOp^Read_20/DisableCopyOnRead^Read_20/ReadVariableOp^Read_21/DisableCopyOnRead^Read_21/ReadVariableOp^Read_22/DisableCopyOnRead^Read_22/ReadVariableOp^Read_23/DisableCopyOnRead^Read_23/ReadVariableOp^Read_24/DisableCopyOnRead^Read_24/ReadVariableOp^Read_3/DisableCopyOnRead^Read_3/ReadVariableOp^Read_4/DisableCopyOnRead^Read_4/ReadVariableOp^Read_5/DisableCopyOnRead^Read_5/ReadVariableOp^Read_6/DisableCopyOnRead^Read_6/ReadVariableOp^Read_7/DisableCopyOnRead^Read_7/ReadVariableOp^Read_8/DisableCopyOnRead^Read_8/ReadVariableOp^Read_9/DisableCopyOnRead^Read_9/ReadVariableOp*
_output_shapes
 "#
identity_51Identity_51:output:0*(
_construction_contextkEagerRuntime*I
_input_shapes8
6: : : : : : : : : : : : : : : : : : : : : : : : : : : 2(
MergeV2CheckpointsMergeV2Checkpoints20
Read/DisableCopyOnReadRead/DisableCopyOnRead2*
Read/ReadVariableOpRead/ReadVariableOp24
Read_1/DisableCopyOnReadRead_1/DisableCopyOnRead2.
Read_1/ReadVariableOpRead_1/ReadVariableOp26
Read_10/DisableCopyOnReadRead_10/DisableCopyOnRead20
Read_10/ReadVariableOpRead_10/ReadVariableOp26
Read_11/DisableCopyOnReadRead_11/DisableCopyOnRead20
Read_11/ReadVariableOpRead_11/ReadVariableOp26
Read_12/DisableCopyOnReadRead_12/DisableCopyOnRead20
Read_12/ReadVariableOpRead_12/ReadVariableOp26
Read_13/DisableCopyOnReadRead_13/DisableCopyOnRead20
Read_13/ReadVariableOpRead_13/ReadVariableOp26
Read_14/DisableCopyOnReadRead_14/DisableCopyOnRead20
Read_14/ReadVariableOpRead_14/ReadVariableOp26
Read_15/DisableCopyOnReadRead_15/DisableCopyOnRead20
Read_15/ReadVariableOpRead_15/ReadVariableOp26
Read_16/DisableCopyOnReadRead_16/DisableCopyOnRead20
Read_16/ReadVariableOpRead_16/ReadVariableOp26
Read_17/DisableCopyOnReadRead_17/DisableCopyOnRead20
Read_17/ReadVariableOpRead_17/ReadVariableOp26
Read_18/DisableCopyOnReadRead_18/DisableCopyOnRead20
Read_18/ReadVariableOpRead_18/ReadVariableOp26
Read_19/DisableCopyOnReadRead_19/DisableCopyOnRead20
Read_19/ReadVariableOpRead_19/ReadVariableOp24
Read_2/DisableCopyOnReadRead_2/DisableCopyOnRead2.
Read_2/ReadVariableOpRead_2/ReadVariableOp26
Read_20/DisableCopyOnReadRead_20/DisableCopyOnRead20
Read_20/ReadVariableOpRead_20/ReadVariableOp26
Read_21/DisableCopyOnReadRead_21/DisableCopyOnRead20
Read_21/ReadVariableOpRead_21/ReadVariableOp26
Read_22/DisableCopyOnReadRead_22/DisableCopyOnRead20
Read_22/ReadVariableOpRead_22/ReadVariableOp26
Read_23/DisableCopyOnReadRead_23/DisableCopyOnRead20
Read_23/ReadVariableOpRead_23/ReadVariableOp26
Read_24/DisableCopyOnReadRead_24/DisableCopyOnRead20
Read_24/ReadVariableOpRead_24/ReadVariableOp24
Read_3/DisableCopyOnReadRead_3/DisableCopyOnRead2.
Read_3/ReadVariableOpRead_3/ReadVariableOp24
Read_4/DisableCopyOnReadRead_4/DisableCopyOnRead2.
Read_4/ReadVariableOpRead_4/ReadVariableOp24
Read_5/DisableCopyOnReadRead_5/DisableCopyOnRead2.
Read_5/ReadVariableOpRead_5/ReadVariableOp24
Read_6/DisableCopyOnReadRead_6/DisableCopyOnRead2.
Read_6/ReadVariableOpRead_6/ReadVariableOp24
Read_7/DisableCopyOnReadRead_7/DisableCopyOnRead2.
Read_7/ReadVariableOpRead_7/ReadVariableOp24
Read_8/DisableCopyOnReadRead_8/DisableCopyOnRead2.
Read_8/ReadVariableOpRead_8/ReadVariableOp24
Read_9/DisableCopyOnReadRead_9/DisableCopyOnRead2.
Read_9/ReadVariableOpRead_9/ReadVariableOp:=9

_output_shapes
: 

_user_specified_nameConst:<8
6
_user_specified_nametraining/Adam/dense_5/bias/v:>:
8
_user_specified_name training/Adam/dense_5/kernel/v:<8
6
_user_specified_nametraining/Adam/dense_4/bias/v:>:
8
_user_specified_name training/Adam/dense_4/kernel/v:<8
6
_user_specified_nametraining/Adam/dense_3/bias/v:>:
8
_user_specified_name training/Adam/dense_3/kernel/v:<8
6
_user_specified_nametraining/Adam/dense_5/bias/m:>:
8
_user_specified_name training/Adam/dense_5/kernel/m:<8
6
_user_specified_nametraining/Adam/dense_4/bias/m:>:
8
_user_specified_name training/Adam/dense_4/kernel/m:<8
6
_user_specified_nametraining/Adam/dense_3/bias/m:>:
8
_user_specified_name training/Adam/dense_3/kernel/m:'#
!
_user_specified_name	count_1:'#
!
_user_specified_name	total_1:;7
5
_user_specified_nametraining/Adam/learning_rate:3
/
-
_user_specified_nametraining/Adam/decay:4	0
.
_user_specified_nametraining/Adam/beta_2:40
.
_user_specified_nametraining/Adam/beta_1:2.
,
_user_specified_nametraining/Adam/iter:,(
&
_user_specified_namedense_5/bias:.*
(
_user_specified_namedense_5/kernel:,(
&
_user_specified_namedense_4/bias:.*
(
_user_specified_namedense_4/kernel:,(
&
_user_specified_namedense_3/bias:.*
(
_user_specified_namedense_3/kernel:C ?

_output_shapes
: 
%
_user_specified_namefile_prefix
�
f
J__inference_leaky_re_lu_2_layer_call_and_return_conditional_losses_1619465

inputs
identityW
	LeakyRelu	LeakyReluinputs*'
_output_shapes
:���������F*
alpha%���>_
IdentityIdentityLeakyRelu:activations:0*
T0*'
_output_shapes
:���������F"
identityIdentity:output:0*(
_construction_contextkEagerRuntime*&
_input_shapes
:���������F:O K
'
_output_shapes
:���������F
 
_user_specified_nameinputs
�

�
D__inference_dense_3_layer_call_and_return_conditional_losses_1619455

inputs6
$matmul_readvariableop_dense_3_kernel:RF1
#biasadd_readvariableop_dense_3_bias:F
identity��BiasAdd/ReadVariableOp�MatMul/ReadVariableOpz
MatMul/ReadVariableOpReadVariableOp$matmul_readvariableop_dense_3_kernel*
_output_shapes

:RF*
dtype0i
MatMulMatMulinputsMatMul/ReadVariableOp:value:0*
T0*'
_output_shapes
:���������Fv
BiasAdd/ReadVariableOpReadVariableOp#biasadd_readvariableop_dense_3_bias*
_output_shapes
:F*
dtype0v
BiasAddBiasAddMatMul:product:0BiasAdd/ReadVariableOp:value:0*
T0*'
_output_shapes
:���������F_
IdentityIdentityBiasAdd:output:0^NoOp*
T0*'
_output_shapes
:���������FS
NoOpNoOp^BiasAdd/ReadVariableOp^MatMul/ReadVariableOp*
_output_shapes
 "
identityIdentity:output:0*(
_construction_contextkEagerRuntime**
_input_shapes
:���������R: : 20
BiasAdd/ReadVariableOpBiasAdd/ReadVariableOp2.
MatMul/ReadVariableOpMatMul/ReadVariableOp:,(
&
_user_specified_namedense_3/bias:.*
(
_user_specified_namedense_3/kernel:O K
'
_output_shapes
:���������R
 
_user_specified_nameinputs
�
f
J__inference_leaky_re_lu_3_layer_call_and_return_conditional_losses_1619492

inputs
identityW
	LeakyRelu	LeakyReluinputs*'
_output_shapes
:���������9*
alpha%���>_
IdentityIdentityLeakyRelu:activations:0*
T0*'
_output_shapes
:���������9"
identityIdentity:output:0*(
_construction_contextkEagerRuntime*&
_input_shapes
:���������9:O K
'
_output_shapes
:���������9
 
_user_specified_nameinputs
�
�
I__inference_sequential_1_layer_call_and_return_conditional_losses_1619298

inputs(
dense_3_dense_3_kernel:RF"
dense_3_dense_3_bias:F(
dense_4_dense_4_kernel:F9"
dense_4_dense_4_bias:9(
dense_5_dense_5_kernel:9y"
dense_5_dense_5_bias:y
identity��dense_3/StatefulPartitionedCall�dense_4/StatefulPartitionedCall�dense_5/StatefulPartitionedCall�
dense_3/StatefulPartitionedCallStatefulPartitionedCallinputsdense_3_dense_3_kerneldense_3_dense_3_bias*
Tin
2*
Tout
2*
_collective_manager_ids
 *'
_output_shapes
:���������F*$
_read_only_resource_inputs
*0
config_proto 

CPU

GPU2*0J 8� *M
fHRF
D__inference_dense_3_layer_call_and_return_conditional_losses_1619197�
leaky_re_lu_2/PartitionedCallPartitionedCall(dense_3/StatefulPartitionedCall:output:0*
Tin
2*
Tout
2*
_collective_manager_ids
 *'
_output_shapes
:���������F* 
_read_only_resource_inputs
 *0
config_proto 

CPU

GPU2*0J 8� *S
fNRL
J__inference_leaky_re_lu_2_layer_call_and_return_conditional_losses_1619205�
dense_4/StatefulPartitionedCallStatefulPartitionedCall&leaky_re_lu_2/PartitionedCall:output:0dense_4_dense_4_kerneldense_4_dense_4_bias*
Tin
2*
Tout
2*
_collective_manager_ids
 *'
_output_shapes
:���������9*$
_read_only_resource_inputs
*0
config_proto 

CPU

GPU2*0J 8� *M
fHRF
D__inference_dense_4_layer_call_and_return_conditional_losses_1619216�
leaky_re_lu_3/PartitionedCallPartitionedCall(dense_4/StatefulPartitionedCall:output:0*
Tin
2*
Tout
2*
_collective_manager_ids
 *'
_output_shapes
:���������9* 
_read_only_resource_inputs
 *0
config_proto 

CPU

GPU2*0J 8� *S
fNRL
J__inference_leaky_re_lu_3_layer_call_and_return_conditional_losses_1619224�
dense_5/StatefulPartitionedCallStatefulPartitionedCall&leaky_re_lu_3/PartitionedCall:output:0dense_5_dense_5_kerneldense_5_dense_5_bias*
Tin
2*
Tout
2*
_collective_manager_ids
 *'
_output_shapes
:���������y*$
_read_only_resource_inputs
*0
config_proto 

CPU

GPU2*0J 8� *M
fHRF
D__inference_dense_5_layer_call_and_return_conditional_losses_1619235w
IdentityIdentity(dense_5/StatefulPartitionedCall:output:0^NoOp*
T0*'
_output_shapes
:���������y�
NoOpNoOp ^dense_3/StatefulPartitionedCall ^dense_4/StatefulPartitionedCall ^dense_5/StatefulPartitionedCall*
_output_shapes
 "
identityIdentity:output:0*(
_construction_contextkEagerRuntime*2
_input_shapes!
:���������R: : : : : : 2B
dense_3/StatefulPartitionedCalldense_3/StatefulPartitionedCall2B
dense_4/StatefulPartitionedCalldense_4/StatefulPartitionedCall2B
dense_5/StatefulPartitionedCalldense_5/StatefulPartitionedCall:,(
&
_user_specified_namedense_5/bias:.*
(
_user_specified_namedense_5/kernel:,(
&
_user_specified_namedense_4/bias:.*
(
_user_specified_namedense_4/kernel:,(
&
_user_specified_namedense_3/bias:.*
(
_user_specified_namedense_3/kernel:O K
'
_output_shapes
:���������R
 
_user_specified_nameinputs
�

�
D__inference_dense_3_layer_call_and_return_conditional_losses_1619197

inputs6
$matmul_readvariableop_dense_3_kernel:RF1
#biasadd_readvariableop_dense_3_bias:F
identity��BiasAdd/ReadVariableOp�MatMul/ReadVariableOpz
MatMul/ReadVariableOpReadVariableOp$matmul_readvariableop_dense_3_kernel*
_output_shapes

:RF*
dtype0i
MatMulMatMulinputsMatMul/ReadVariableOp:value:0*
T0*'
_output_shapes
:���������Fv
BiasAdd/ReadVariableOpReadVariableOp#biasadd_readvariableop_dense_3_bias*
_output_shapes
:F*
dtype0v
BiasAddBiasAddMatMul:product:0BiasAdd/ReadVariableOp:value:0*
T0*'
_output_shapes
:���������F_
IdentityIdentityBiasAdd:output:0^NoOp*
T0*'
_output_shapes
:���������FS
NoOpNoOp^BiasAdd/ReadVariableOp^MatMul/ReadVariableOp*
_output_shapes
 "
identityIdentity:output:0*(
_construction_contextkEagerRuntime**
_input_shapes
:���������R: : 20
BiasAdd/ReadVariableOpBiasAdd/ReadVariableOp2.
MatMul/ReadVariableOpMatMul/ReadVariableOp:,(
&
_user_specified_namedense_3/bias:.*
(
_user_specified_namedense_3/kernel:O K
'
_output_shapes
:���������R
 
_user_specified_nameinputs
�

�
D__inference_dense_5_layer_call_and_return_conditional_losses_1619509

inputs6
$matmul_readvariableop_dense_5_kernel:9y1
#biasadd_readvariableop_dense_5_bias:y
identity��BiasAdd/ReadVariableOp�MatMul/ReadVariableOpz
MatMul/ReadVariableOpReadVariableOp$matmul_readvariableop_dense_5_kernel*
_output_shapes

:9y*
dtype0i
MatMulMatMulinputsMatMul/ReadVariableOp:value:0*
T0*'
_output_shapes
:���������yv
BiasAdd/ReadVariableOpReadVariableOp#biasadd_readvariableop_dense_5_bias*
_output_shapes
:y*
dtype0v
BiasAddBiasAddMatMul:product:0BiasAdd/ReadVariableOp:value:0*
T0*'
_output_shapes
:���������y_
IdentityIdentityBiasAdd:output:0^NoOp*
T0*'
_output_shapes
:���������yS
NoOpNoOp^BiasAdd/ReadVariableOp^MatMul/ReadVariableOp*
_output_shapes
 "
identityIdentity:output:0*(
_construction_contextkEagerRuntime**
_input_shapes
:���������9: : 20
BiasAdd/ReadVariableOpBiasAdd/ReadVariableOp2.
MatMul/ReadVariableOpMatMul/ReadVariableOp:,(
&
_user_specified_namedense_5/bias:.*
(
_user_specified_namedense_5/kernel:O K
'
_output_shapes
:���������9
 
_user_specified_nameinputs
�
�
)__inference_dense_4_layer_call_fn_1619472

inputs 
dense_4_kernel:F9
dense_4_bias:9
identity��StatefulPartitionedCall�
StatefulPartitionedCallStatefulPartitionedCallinputsdense_4_kerneldense_4_bias*
Tin
2*
Tout
2*
_collective_manager_ids
 *'
_output_shapes
:���������9*$
_read_only_resource_inputs
*0
config_proto 

CPU

GPU2*0J 8� *M
fHRF
D__inference_dense_4_layer_call_and_return_conditional_losses_1619216o
IdentityIdentity StatefulPartitionedCall:output:0^NoOp*
T0*'
_output_shapes
:���������9<
NoOpNoOp^StatefulPartitionedCall*
_output_shapes
 "
identityIdentity:output:0*(
_construction_contextkEagerRuntime**
_input_shapes
:���������F: : 22
StatefulPartitionedCallStatefulPartitionedCall:,(
&
_user_specified_namedense_4/bias:.*
(
_user_specified_namedense_4/kernel:O K
'
_output_shapes
:���������F
 
_user_specified_nameinputs
�
�
.__inference_sequential_1_layer_call_fn_1619281
dense_3_input 
dense_3_kernel:RF
dense_3_bias:F 
dense_4_kernel:F9
dense_4_bias:9 
dense_5_kernel:9y
dense_5_bias:y
identity��StatefulPartitionedCall�
StatefulPartitionedCallStatefulPartitionedCalldense_3_inputdense_3_kerneldense_3_biasdense_4_kerneldense_4_biasdense_5_kerneldense_5_bias*
Tin
	2*
Tout
2*
_collective_manager_ids
 *'
_output_shapes
:���������y*(
_read_only_resource_inputs

*0
config_proto 

CPU

GPU2*0J 8� *R
fMRK
I__inference_sequential_1_layer_call_and_return_conditional_losses_1619272o
IdentityIdentity StatefulPartitionedCall:output:0^NoOp*
T0*'
_output_shapes
:���������y<
NoOpNoOp^StatefulPartitionedCall*
_output_shapes
 "
identityIdentity:output:0*(
_construction_contextkEagerRuntime*2
_input_shapes!
:���������R: : : : : : 22
StatefulPartitionedCallStatefulPartitionedCall:,(
&
_user_specified_namedense_5/bias:.*
(
_user_specified_namedense_5/kernel:,(
&
_user_specified_namedense_4/bias:.*
(
_user_specified_namedense_4/kernel:,(
&
_user_specified_namedense_3/bias:.*
(
_user_specified_namedense_3/kernel:V R
'
_output_shapes
:���������R
'
_user_specified_namedense_3_input
�

�
D__inference_dense_4_layer_call_and_return_conditional_losses_1619482

inputs6
$matmul_readvariableop_dense_4_kernel:F91
#biasadd_readvariableop_dense_4_bias:9
identity��BiasAdd/ReadVariableOp�MatMul/ReadVariableOpz
MatMul/ReadVariableOpReadVariableOp$matmul_readvariableop_dense_4_kernel*
_output_shapes

:F9*
dtype0i
MatMulMatMulinputsMatMul/ReadVariableOp:value:0*
T0*'
_output_shapes
:���������9v
BiasAdd/ReadVariableOpReadVariableOp#biasadd_readvariableop_dense_4_bias*
_output_shapes
:9*
dtype0v
BiasAddBiasAddMatMul:product:0BiasAdd/ReadVariableOp:value:0*
T0*'
_output_shapes
:���������9_
IdentityIdentityBiasAdd:output:0^NoOp*
T0*'
_output_shapes
:���������9S
NoOpNoOp^BiasAdd/ReadVariableOp^MatMul/ReadVariableOp*
_output_shapes
 "
identityIdentity:output:0*(
_construction_contextkEagerRuntime**
_input_shapes
:���������F: : 20
BiasAdd/ReadVariableOpBiasAdd/ReadVariableOp2.
MatMul/ReadVariableOpMatMul/ReadVariableOp:,(
&
_user_specified_namedense_4/bias:.*
(
_user_specified_namedense_4/kernel:O K
'
_output_shapes
:���������F
 
_user_specified_nameinputs
�
�
)__inference_dense_5_layer_call_fn_1619499

inputs 
dense_5_kernel:9y
dense_5_bias:y
identity��StatefulPartitionedCall�
StatefulPartitionedCallStatefulPartitionedCallinputsdense_5_kerneldense_5_bias*
Tin
2*
Tout
2*
_collective_manager_ids
 *'
_output_shapes
:���������y*$
_read_only_resource_inputs
*0
config_proto 

CPU

GPU2*0J 8� *M
fHRF
D__inference_dense_5_layer_call_and_return_conditional_losses_1619235o
IdentityIdentity StatefulPartitionedCall:output:0^NoOp*
T0*'
_output_shapes
:���������y<
NoOpNoOp^StatefulPartitionedCall*
_output_shapes
 "
identityIdentity:output:0*(
_construction_contextkEagerRuntime**
_input_shapes
:���������9: : 22
StatefulPartitionedCallStatefulPartitionedCall:,(
&
_user_specified_namedense_5/bias:.*
(
_user_specified_namedense_5/kernel:O K
'
_output_shapes
:���������9
 
_user_specified_nameinputs
�$
�
"__inference__wrapped_model_1619185
dense_3_inputK
9sequential_1_dense_3_matmul_readvariableop_dense_3_kernel:RFF
8sequential_1_dense_3_biasadd_readvariableop_dense_3_bias:FK
9sequential_1_dense_4_matmul_readvariableop_dense_4_kernel:F9F
8sequential_1_dense_4_biasadd_readvariableop_dense_4_bias:9K
9sequential_1_dense_5_matmul_readvariableop_dense_5_kernel:9yF
8sequential_1_dense_5_biasadd_readvariableop_dense_5_bias:y
identity��+sequential_1/dense_3/BiasAdd/ReadVariableOp�*sequential_1/dense_3/MatMul/ReadVariableOp�+sequential_1/dense_4/BiasAdd/ReadVariableOp�*sequential_1/dense_4/MatMul/ReadVariableOp�+sequential_1/dense_5/BiasAdd/ReadVariableOp�*sequential_1/dense_5/MatMul/ReadVariableOp�
*sequential_1/dense_3/MatMul/ReadVariableOpReadVariableOp9sequential_1_dense_3_matmul_readvariableop_dense_3_kernel*
_output_shapes

:RF*
dtype0�
sequential_1/dense_3/MatMulMatMuldense_3_input2sequential_1/dense_3/MatMul/ReadVariableOp:value:0*
T0*'
_output_shapes
:���������F�
+sequential_1/dense_3/BiasAdd/ReadVariableOpReadVariableOp8sequential_1_dense_3_biasadd_readvariableop_dense_3_bias*
_output_shapes
:F*
dtype0�
sequential_1/dense_3/BiasAddBiasAdd%sequential_1/dense_3/MatMul:product:03sequential_1/dense_3/BiasAdd/ReadVariableOp:value:0*
T0*'
_output_shapes
:���������F�
$sequential_1/leaky_re_lu_2/LeakyRelu	LeakyRelu%sequential_1/dense_3/BiasAdd:output:0*'
_output_shapes
:���������F*
alpha%���>�
*sequential_1/dense_4/MatMul/ReadVariableOpReadVariableOp9sequential_1_dense_4_matmul_readvariableop_dense_4_kernel*
_output_shapes

:F9*
dtype0�
sequential_1/dense_4/MatMulMatMul2sequential_1/leaky_re_lu_2/LeakyRelu:activations:02sequential_1/dense_4/MatMul/ReadVariableOp:value:0*
T0*'
_output_shapes
:���������9�
+sequential_1/dense_4/BiasAdd/ReadVariableOpReadVariableOp8sequential_1_dense_4_biasadd_readvariableop_dense_4_bias*
_output_shapes
:9*
dtype0�
sequential_1/dense_4/BiasAddBiasAdd%sequential_1/dense_4/MatMul:product:03sequential_1/dense_4/BiasAdd/ReadVariableOp:value:0*
T0*'
_output_shapes
:���������9�
$sequential_1/leaky_re_lu_3/LeakyRelu	LeakyRelu%sequential_1/dense_4/BiasAdd:output:0*'
_output_shapes
:���������9*
alpha%���>�
*sequential_1/dense_5/MatMul/ReadVariableOpReadVariableOp9sequential_1_dense_5_matmul_readvariableop_dense_5_kernel*
_output_shapes

:9y*
dtype0�
sequential_1/dense_5/MatMulMatMul2sequential_1/leaky_re_lu_3/LeakyRelu:activations:02sequential_1/dense_5/MatMul/ReadVariableOp:value:0*
T0*'
_output_shapes
:���������y�
+sequential_1/dense_5/BiasAdd/ReadVariableOpReadVariableOp8sequential_1_dense_5_biasadd_readvariableop_dense_5_bias*
_output_shapes
:y*
dtype0�
sequential_1/dense_5/BiasAddBiasAdd%sequential_1/dense_5/MatMul:product:03sequential_1/dense_5/BiasAdd/ReadVariableOp:value:0*
T0*'
_output_shapes
:���������yt
IdentityIdentity%sequential_1/dense_5/BiasAdd:output:0^NoOp*
T0*'
_output_shapes
:���������y�
NoOpNoOp,^sequential_1/dense_3/BiasAdd/ReadVariableOp+^sequential_1/dense_3/MatMul/ReadVariableOp,^sequential_1/dense_4/BiasAdd/ReadVariableOp+^sequential_1/dense_4/MatMul/ReadVariableOp,^sequential_1/dense_5/BiasAdd/ReadVariableOp+^sequential_1/dense_5/MatMul/ReadVariableOp*
_output_shapes
 "
identityIdentity:output:0*(
_construction_contextkEagerRuntime*2
_input_shapes!
:���������R: : : : : : 2Z
+sequential_1/dense_3/BiasAdd/ReadVariableOp+sequential_1/dense_3/BiasAdd/ReadVariableOp2X
*sequential_1/dense_3/MatMul/ReadVariableOp*sequential_1/dense_3/MatMul/ReadVariableOp2Z
+sequential_1/dense_4/BiasAdd/ReadVariableOp+sequential_1/dense_4/BiasAdd/ReadVariableOp2X
*sequential_1/dense_4/MatMul/ReadVariableOp*sequential_1/dense_4/MatMul/ReadVariableOp2Z
+sequential_1/dense_5/BiasAdd/ReadVariableOp+sequential_1/dense_5/BiasAdd/ReadVariableOp2X
*sequential_1/dense_5/MatMul/ReadVariableOp*sequential_1/dense_5/MatMul/ReadVariableOp:,(
&
_user_specified_namedense_5/bias:.*
(
_user_specified_namedense_5/kernel:,(
&
_user_specified_namedense_4/bias:.*
(
_user_specified_namedense_4/kernel:,(
&
_user_specified_namedense_3/bias:.*
(
_user_specified_namedense_3/kernel:V R
'
_output_shapes
:���������R
'
_user_specified_namedense_3_input
�
�
I__inference_sequential_1_layer_call_and_return_conditional_losses_1619240
dense_3_input(
dense_3_dense_3_kernel:RF"
dense_3_dense_3_bias:F(
dense_4_dense_4_kernel:F9"
dense_4_dense_4_bias:9(
dense_5_dense_5_kernel:9y"
dense_5_dense_5_bias:y
identity��dense_3/StatefulPartitionedCall�dense_4/StatefulPartitionedCall�dense_5/StatefulPartitionedCall�
dense_3/StatefulPartitionedCallStatefulPartitionedCalldense_3_inputdense_3_dense_3_kerneldense_3_dense_3_bias*
Tin
2*
Tout
2*
_collective_manager_ids
 *'
_output_shapes
:���������F*$
_read_only_resource_inputs
*0
config_proto 

CPU

GPU2*0J 8� *M
fHRF
D__inference_dense_3_layer_call_and_return_conditional_losses_1619197�
leaky_re_lu_2/PartitionedCallPartitionedCall(dense_3/StatefulPartitionedCall:output:0*
Tin
2*
Tout
2*
_collective_manager_ids
 *'
_output_shapes
:���������F* 
_read_only_resource_inputs
 *0
config_proto 

CPU

GPU2*0J 8� *S
fNRL
J__inference_leaky_re_lu_2_layer_call_and_return_conditional_losses_1619205�
dense_4/StatefulPartitionedCallStatefulPartitionedCall&leaky_re_lu_2/PartitionedCall:output:0dense_4_dense_4_kerneldense_4_dense_4_bias*
Tin
2*
Tout
2*
_collective_manager_ids
 *'
_output_shapes
:���������9*$
_read_only_resource_inputs
*0
config_proto 

CPU

GPU2*0J 8� *M
fHRF
D__inference_dense_4_layer_call_and_return_conditional_losses_1619216�
leaky_re_lu_3/PartitionedCallPartitionedCall(dense_4/StatefulPartitionedCall:output:0*
Tin
2*
Tout
2*
_collective_manager_ids
 *'
_output_shapes
:���������9* 
_read_only_resource_inputs
 *0
config_proto 

CPU

GPU2*0J 8� *S
fNRL
J__inference_leaky_re_lu_3_layer_call_and_return_conditional_losses_1619224�
dense_5/StatefulPartitionedCallStatefulPartitionedCall&leaky_re_lu_3/PartitionedCall:output:0dense_5_dense_5_kerneldense_5_dense_5_bias*
Tin
2*
Tout
2*
_collective_manager_ids
 *'
_output_shapes
:���������y*$
_read_only_resource_inputs
*0
config_proto 

CPU

GPU2*0J 8� *M
fHRF
D__inference_dense_5_layer_call_and_return_conditional_losses_1619235w
IdentityIdentity(dense_5/StatefulPartitionedCall:output:0^NoOp*
T0*'
_output_shapes
:���������y�
NoOpNoOp ^dense_3/StatefulPartitionedCall ^dense_4/StatefulPartitionedCall ^dense_5/StatefulPartitionedCall*
_output_shapes
 "
identityIdentity:output:0*(
_construction_contextkEagerRuntime*2
_input_shapes!
:���������R: : : : : : 2B
dense_3/StatefulPartitionedCalldense_3/StatefulPartitionedCall2B
dense_4/StatefulPartitionedCalldense_4/StatefulPartitionedCall2B
dense_5/StatefulPartitionedCalldense_5/StatefulPartitionedCall:,(
&
_user_specified_namedense_5/bias:.*
(
_user_specified_namedense_5/kernel:,(
&
_user_specified_namedense_4/bias:.*
(
_user_specified_namedense_4/kernel:,(
&
_user_specified_namedense_3/bias:.*
(
_user_specified_namedense_3/kernel:V R
'
_output_shapes
:���������R
'
_user_specified_namedense_3_input
�z
�
#__inference__traced_restore_1619765
file_prefix1
assignvariableop_dense_3_kernel:RF-
assignvariableop_1_dense_3_bias:F3
!assignvariableop_2_dense_4_kernel:F9-
assignvariableop_3_dense_4_bias:93
!assignvariableop_4_dense_5_kernel:9y-
assignvariableop_5_dense_5_bias:y/
%assignvariableop_6_training_adam_iter:	 1
'assignvariableop_7_training_adam_beta_1: 1
'assignvariableop_8_training_adam_beta_2: 0
&assignvariableop_9_training_adam_decay: 9
/assignvariableop_10_training_adam_learning_rate: %
assignvariableop_11_total_1: %
assignvariableop_12_count_1: D
2assignvariableop_13_training_adam_dense_3_kernel_m:RF>
0assignvariableop_14_training_adam_dense_3_bias_m:FD
2assignvariableop_15_training_adam_dense_4_kernel_m:F9>
0assignvariableop_16_training_adam_dense_4_bias_m:9D
2assignvariableop_17_training_adam_dense_5_kernel_m:9y>
0assignvariableop_18_training_adam_dense_5_bias_m:yD
2assignvariableop_19_training_adam_dense_3_kernel_v:RF>
0assignvariableop_20_training_adam_dense_3_bias_v:FD
2assignvariableop_21_training_adam_dense_4_kernel_v:F9>
0assignvariableop_22_training_adam_dense_4_bias_v:9D
2assignvariableop_23_training_adam_dense_5_kernel_v:9y>
0assignvariableop_24_training_adam_dense_5_bias_v:y
identity_26��AssignVariableOp�AssignVariableOp_1�AssignVariableOp_10�AssignVariableOp_11�AssignVariableOp_12�AssignVariableOp_13�AssignVariableOp_14�AssignVariableOp_15�AssignVariableOp_16�AssignVariableOp_17�AssignVariableOp_18�AssignVariableOp_19�AssignVariableOp_2�AssignVariableOp_20�AssignVariableOp_21�AssignVariableOp_22�AssignVariableOp_23�AssignVariableOp_24�AssignVariableOp_3�AssignVariableOp_4�AssignVariableOp_5�AssignVariableOp_6�AssignVariableOp_7�AssignVariableOp_8�AssignVariableOp_9�
RestoreV2/tensor_namesConst"/device:CPU:0*
_output_shapes
:*
dtype0*�
value�B�B6layer_with_weights-0/kernel/.ATTRIBUTES/VARIABLE_VALUEB4layer_with_weights-0/bias/.ATTRIBUTES/VARIABLE_VALUEB6layer_with_weights-1/kernel/.ATTRIBUTES/VARIABLE_VALUEB4layer_with_weights-1/bias/.ATTRIBUTES/VARIABLE_VALUEB6layer_with_weights-2/kernel/.ATTRIBUTES/VARIABLE_VALUEB4layer_with_weights-2/bias/.ATTRIBUTES/VARIABLE_VALUEB)optimizer/iter/.ATTRIBUTES/VARIABLE_VALUEB+optimizer/beta_1/.ATTRIBUTES/VARIABLE_VALUEB+optimizer/beta_2/.ATTRIBUTES/VARIABLE_VALUEB*optimizer/decay/.ATTRIBUTES/VARIABLE_VALUEB2optimizer/learning_rate/.ATTRIBUTES/VARIABLE_VALUEB4keras_api/metrics/0/total/.ATTRIBUTES/VARIABLE_VALUEB4keras_api/metrics/0/count/.ATTRIBUTES/VARIABLE_VALUEBRlayer_with_weights-0/kernel/.OPTIMIZER_SLOT/optimizer/m/.ATTRIBUTES/VARIABLE_VALUEBPlayer_with_weights-0/bias/.OPTIMIZER_SLOT/optimizer/m/.ATTRIBUTES/VARIABLE_VALUEBRlayer_with_weights-1/kernel/.OPTIMIZER_SLOT/optimizer/m/.ATTRIBUTES/VARIABLE_VALUEBPlayer_with_weights-1/bias/.OPTIMIZER_SLOT/optimizer/m/.ATTRIBUTES/VARIABLE_VALUEBRlayer_with_weights-2/kernel/.OPTIMIZER_SLOT/optimizer/m/.ATTRIBUTES/VARIABLE_VALUEBPlayer_with_weights-2/bias/.OPTIMIZER_SLOT/optimizer/m/.ATTRIBUTES/VARIABLE_VALUEBRlayer_with_weights-0/kernel/.OPTIMIZER_SLOT/optimizer/v/.ATTRIBUTES/VARIABLE_VALUEBPlayer_with_weights-0/bias/.OPTIMIZER_SLOT/optimizer/v/.ATTRIBUTES/VARIABLE_VALUEBRlayer_with_weights-1/kernel/.OPTIMIZER_SLOT/optimizer/v/.ATTRIBUTES/VARIABLE_VALUEBPlayer_with_weights-1/bias/.OPTIMIZER_SLOT/optimizer/v/.ATTRIBUTES/VARIABLE_VALUEBRlayer_with_weights-2/kernel/.OPTIMIZER_SLOT/optimizer/v/.ATTRIBUTES/VARIABLE_VALUEBPlayer_with_weights-2/bias/.OPTIMIZER_SLOT/optimizer/v/.ATTRIBUTES/VARIABLE_VALUEB_CHECKPOINTABLE_OBJECT_GRAPH�
RestoreV2/shape_and_slicesConst"/device:CPU:0*
_output_shapes
:*
dtype0*G
value>B<B B B B B B B B B B B B B B B B B B B B B B B B B B �
	RestoreV2	RestoreV2file_prefixRestoreV2/tensor_names:output:0#RestoreV2/shape_and_slices:output:0"/device:CPU:0*|
_output_shapesj
h::::::::::::::::::::::::::*(
dtypes
2	[
IdentityIdentityRestoreV2:tensors:0"/device:CPU:0*
T0*
_output_shapes
:�
AssignVariableOpAssignVariableOpassignvariableop_dense_3_kernelIdentity:output:0"/device:CPU:0*&
 _has_manual_control_dependencies(*
_output_shapes
 *
dtype0]

Identity_1IdentityRestoreV2:tensors:1"/device:CPU:0*
T0*
_output_shapes
:�
AssignVariableOp_1AssignVariableOpassignvariableop_1_dense_3_biasIdentity_1:output:0"/device:CPU:0*&
 _has_manual_control_dependencies(*
_output_shapes
 *
dtype0]

Identity_2IdentityRestoreV2:tensors:2"/device:CPU:0*
T0*
_output_shapes
:�
AssignVariableOp_2AssignVariableOp!assignvariableop_2_dense_4_kernelIdentity_2:output:0"/device:CPU:0*&
 _has_manual_control_dependencies(*
_output_shapes
 *
dtype0]

Identity_3IdentityRestoreV2:tensors:3"/device:CPU:0*
T0*
_output_shapes
:�
AssignVariableOp_3AssignVariableOpassignvariableop_3_dense_4_biasIdentity_3:output:0"/device:CPU:0*&
 _has_manual_control_dependencies(*
_output_shapes
 *
dtype0]

Identity_4IdentityRestoreV2:tensors:4"/device:CPU:0*
T0*
_output_shapes
:�
AssignVariableOp_4AssignVariableOp!assignvariableop_4_dense_5_kernelIdentity_4:output:0"/device:CPU:0*&
 _has_manual_control_dependencies(*
_output_shapes
 *
dtype0]

Identity_5IdentityRestoreV2:tensors:5"/device:CPU:0*
T0*
_output_shapes
:�
AssignVariableOp_5AssignVariableOpassignvariableop_5_dense_5_biasIdentity_5:output:0"/device:CPU:0*&
 _has_manual_control_dependencies(*
_output_shapes
 *
dtype0]

Identity_6IdentityRestoreV2:tensors:6"/device:CPU:0*
T0	*
_output_shapes
:�
AssignVariableOp_6AssignVariableOp%assignvariableop_6_training_adam_iterIdentity_6:output:0"/device:CPU:0*&
 _has_manual_control_dependencies(*
_output_shapes
 *
dtype0	]

Identity_7IdentityRestoreV2:tensors:7"/device:CPU:0*
T0*
_output_shapes
:�
AssignVariableOp_7AssignVariableOp'assignvariableop_7_training_adam_beta_1Identity_7:output:0"/device:CPU:0*&
 _has_manual_control_dependencies(*
_output_shapes
 *
dtype0]

Identity_8IdentityRestoreV2:tensors:8"/device:CPU:0*
T0*
_output_shapes
:�
AssignVariableOp_8AssignVariableOp'assignvariableop_8_training_adam_beta_2Identity_8:output:0"/device:CPU:0*&
 _has_manual_control_dependencies(*
_output_shapes
 *
dtype0]

Identity_9IdentityRestoreV2:tensors:9"/device:CPU:0*
T0*
_output_shapes
:�
AssignVariableOp_9AssignVariableOp&assignvariableop_9_training_adam_decayIdentity_9:output:0"/device:CPU:0*&
 _has_manual_control_dependencies(*
_output_shapes
 *
dtype0_
Identity_10IdentityRestoreV2:tensors:10"/device:CPU:0*
T0*
_output_shapes
:�
AssignVariableOp_10AssignVariableOp/assignvariableop_10_training_adam_learning_rateIdentity_10:output:0"/device:CPU:0*&
 _has_manual_control_dependencies(*
_output_shapes
 *
dtype0_
Identity_11IdentityRestoreV2:tensors:11"/device:CPU:0*
T0*
_output_shapes
:�
AssignVariableOp_11AssignVariableOpassignvariableop_11_total_1Identity_11:output:0"/device:CPU:0*&
 _has_manual_control_dependencies(*
_output_shapes
 *
dtype0_
Identity_12IdentityRestoreV2:tensors:12"/device:CPU:0*
T0*
_output_shapes
:�
AssignVariableOp_12AssignVariableOpassignvariableop_12_count_1Identity_12:output:0"/device:CPU:0*&
 _has_manual_control_dependencies(*
_output_shapes
 *
dtype0_
Identity_13IdentityRestoreV2:tensors:13"/device:CPU:0*
T0*
_output_shapes
:�
AssignVariableOp_13AssignVariableOp2assignvariableop_13_training_adam_dense_3_kernel_mIdentity_13:output:0"/device:CPU:0*&
 _has_manual_control_dependencies(*
_output_shapes
 *
dtype0_
Identity_14IdentityRestoreV2:tensors:14"/device:CPU:0*
T0*
_output_shapes
:�
AssignVariableOp_14AssignVariableOp0assignvariableop_14_training_adam_dense_3_bias_mIdentity_14:output:0"/device:CPU:0*&
 _has_manual_control_dependencies(*
_output_shapes
 *
dtype0_
Identity_15IdentityRestoreV2:tensors:15"/device:CPU:0*
T0*
_output_shapes
:�
AssignVariableOp_15AssignVariableOp2assignvariableop_15_training_adam_dense_4_kernel_mIdentity_15:output:0"/device:CPU:0*&
 _has_manual_control_dependencies(*
_output_shapes
 *
dtype0_
Identity_16IdentityRestoreV2:tensors:16"/device:CPU:0*
T0*
_output_shapes
:�
AssignVariableOp_16AssignVariableOp0assignvariableop_16_training_adam_dense_4_bias_mIdentity_16:output:0"/device:CPU:0*&
 _has_manual_control_dependencies(*
_output_shapes
 *
dtype0_
Identity_17IdentityRestoreV2:tensors:17"/device:CPU:0*
T0*
_output_shapes
:�
AssignVariableOp_17AssignVariableOp2assignvariableop_17_training_adam_dense_5_kernel_mIdentity_17:output:0"/device:CPU:0*&
 _has_manual_control_dependencies(*
_output_shapes
 *
dtype0_
Identity_18IdentityRestoreV2:tensors:18"/device:CPU:0*
T0*
_output_shapes
:�
AssignVariableOp_18AssignVariableOp0assignvariableop_18_training_adam_dense_5_bias_mIdentity_18:output:0"/device:CPU:0*&
 _has_manual_control_dependencies(*
_output_shapes
 *
dtype0_
Identity_19IdentityRestoreV2:tensors:19"/device:CPU:0*
T0*
_output_shapes
:�
AssignVariableOp_19AssignVariableOp2assignvariableop_19_training_adam_dense_3_kernel_vIdentity_19:output:0"/device:CPU:0*&
 _has_manual_control_dependencies(*
_output_shapes
 *
dtype0_
Identity_20IdentityRestoreV2:tensors:20"/device:CPU:0*
T0*
_output_shapes
:�
AssignVariableOp_20AssignVariableOp0assignvariableop_20_training_adam_dense_3_bias_vIdentity_20:output:0"/device:CPU:0*&
 _has_manual_control_dependencies(*
_output_shapes
 *
dtype0_
Identity_21IdentityRestoreV2:tensors:21"/device:CPU:0*
T0*
_output_shapes
:�
AssignVariableOp_21AssignVariableOp2assignvariableop_21_training_adam_dense_4_kernel_vIdentity_21:output:0"/device:CPU:0*&
 _has_manual_control_dependencies(*
_output_shapes
 *
dtype0_
Identity_22IdentityRestoreV2:tensors:22"/device:CPU:0*
T0*
_output_shapes
:�
AssignVariableOp_22AssignVariableOp0assignvariableop_22_training_adam_dense_4_bias_vIdentity_22:output:0"/device:CPU:0*&
 _has_manual_control_dependencies(*
_output_shapes
 *
dtype0_
Identity_23IdentityRestoreV2:tensors:23"/device:CPU:0*
T0*
_output_shapes
:�
AssignVariableOp_23AssignVariableOp2assignvariableop_23_training_adam_dense_5_kernel_vIdentity_23:output:0"/device:CPU:0*&
 _has_manual_control_dependencies(*
_output_shapes
 *
dtype0_
Identity_24IdentityRestoreV2:tensors:24"/device:CPU:0*
T0*
_output_shapes
:�
AssignVariableOp_24AssignVariableOp0assignvariableop_24_training_adam_dense_5_bias_vIdentity_24:output:0"/device:CPU:0*&
 _has_manual_control_dependencies(*
_output_shapes
 *
dtype0Y
NoOpNoOp"/device:CPU:0*&
 _has_manual_control_dependencies(*
_output_shapes
 �
Identity_25Identityfile_prefix^AssignVariableOp^AssignVariableOp_1^AssignVariableOp_10^AssignVariableOp_11^AssignVariableOp_12^AssignVariableOp_13^AssignVariableOp_14^AssignVariableOp_15^AssignVariableOp_16^AssignVariableOp_17^AssignVariableOp_18^AssignVariableOp_19^AssignVariableOp_2^AssignVariableOp_20^AssignVariableOp_21^AssignVariableOp_22^AssignVariableOp_23^AssignVariableOp_24^AssignVariableOp_3^AssignVariableOp_4^AssignVariableOp_5^AssignVariableOp_6^AssignVariableOp_7^AssignVariableOp_8^AssignVariableOp_9^NoOp"/device:CPU:0*
T0*
_output_shapes
: W
Identity_26IdentityIdentity_25:output:0^NoOp_1*
T0*
_output_shapes
: �
NoOp_1NoOp^AssignVariableOp^AssignVariableOp_1^AssignVariableOp_10^AssignVariableOp_11^AssignVariableOp_12^AssignVariableOp_13^AssignVariableOp_14^AssignVariableOp_15^AssignVariableOp_16^AssignVariableOp_17^AssignVariableOp_18^AssignVariableOp_19^AssignVariableOp_2^AssignVariableOp_20^AssignVariableOp_21^AssignVariableOp_22^AssignVariableOp_23^AssignVariableOp_24^AssignVariableOp_3^AssignVariableOp_4^AssignVariableOp_5^AssignVariableOp_6^AssignVariableOp_7^AssignVariableOp_8^AssignVariableOp_9*
_output_shapes
 "#
identity_26Identity_26:output:0*(
_construction_contextkEagerRuntime*G
_input_shapes6
4: : : : : : : : : : : : : : : : : : : : : : : : : : 2*
AssignVariableOp_10AssignVariableOp_102*
AssignVariableOp_11AssignVariableOp_112*
AssignVariableOp_12AssignVariableOp_122*
AssignVariableOp_13AssignVariableOp_132*
AssignVariableOp_14AssignVariableOp_142*
AssignVariableOp_15AssignVariableOp_152*
AssignVariableOp_16AssignVariableOp_162*
AssignVariableOp_17AssignVariableOp_172*
AssignVariableOp_18AssignVariableOp_182*
AssignVariableOp_19AssignVariableOp_192(
AssignVariableOp_1AssignVariableOp_12*
AssignVariableOp_20AssignVariableOp_202*
AssignVariableOp_21AssignVariableOp_212*
AssignVariableOp_22AssignVariableOp_222*
AssignVariableOp_23AssignVariableOp_232*
AssignVariableOp_24AssignVariableOp_242(
AssignVariableOp_2AssignVariableOp_22(
AssignVariableOp_3AssignVariableOp_32(
AssignVariableOp_4AssignVariableOp_42(
AssignVariableOp_5AssignVariableOp_52(
AssignVariableOp_6AssignVariableOp_62(
AssignVariableOp_7AssignVariableOp_72(
AssignVariableOp_8AssignVariableOp_82(
AssignVariableOp_9AssignVariableOp_92$
AssignVariableOpAssignVariableOp:<8
6
_user_specified_nametraining/Adam/dense_5/bias/v:>:
8
_user_specified_name training/Adam/dense_5/kernel/v:<8
6
_user_specified_nametraining/Adam/dense_4/bias/v:>:
8
_user_specified_name training/Adam/dense_4/kernel/v:<8
6
_user_specified_nametraining/Adam/dense_3/bias/v:>:
8
_user_specified_name training/Adam/dense_3/kernel/v:<8
6
_user_specified_nametraining/Adam/dense_5/bias/m:>:
8
_user_specified_name training/Adam/dense_5/kernel/m:<8
6
_user_specified_nametraining/Adam/dense_4/bias/m:>:
8
_user_specified_name training/Adam/dense_4/kernel/m:<8
6
_user_specified_nametraining/Adam/dense_3/bias/m:>:
8
_user_specified_name training/Adam/dense_3/kernel/m:'#
!
_user_specified_name	count_1:'#
!
_user_specified_name	total_1:;7
5
_user_specified_nametraining/Adam/learning_rate:3
/
-
_user_specified_nametraining/Adam/decay:4	0
.
_user_specified_nametraining/Adam/beta_2:40
.
_user_specified_nametraining/Adam/beta_1:2.
,
_user_specified_nametraining/Adam/iter:,(
&
_user_specified_namedense_5/bias:.*
(
_user_specified_namedense_5/kernel:,(
&
_user_specified_namedense_4/bias:.*
(
_user_specified_namedense_4/kernel:,(
&
_user_specified_namedense_3/bias:.*
(
_user_specified_namedense_3/kernel:C ?

_output_shapes
: 
%
_user_specified_namefile_prefix
�
�
I__inference_sequential_1_layer_call_and_return_conditional_losses_1619272

inputs(
dense_3_dense_3_kernel:RF"
dense_3_dense_3_bias:F(
dense_4_dense_4_kernel:F9"
dense_4_dense_4_bias:9(
dense_5_dense_5_kernel:9y"
dense_5_dense_5_bias:y
identity��dense_3/StatefulPartitionedCall�dense_4/StatefulPartitionedCall�dense_5/StatefulPartitionedCall�
dense_3/StatefulPartitionedCallStatefulPartitionedCallinputsdense_3_dense_3_kerneldense_3_dense_3_bias*
Tin
2*
Tout
2*
_collective_manager_ids
 *'
_output_shapes
:���������F*$
_read_only_resource_inputs
*0
config_proto 

CPU

GPU2*0J 8� *M
fHRF
D__inference_dense_3_layer_call_and_return_conditional_losses_1619197�
leaky_re_lu_2/PartitionedCallPartitionedCall(dense_3/StatefulPartitionedCall:output:0*
Tin
2*
Tout
2*
_collective_manager_ids
 *'
_output_shapes
:���������F* 
_read_only_resource_inputs
 *0
config_proto 

CPU

GPU2*0J 8� *S
fNRL
J__inference_leaky_re_lu_2_layer_call_and_return_conditional_losses_1619205�
dense_4/StatefulPartitionedCallStatefulPartitionedCall&leaky_re_lu_2/PartitionedCall:output:0dense_4_dense_4_kerneldense_4_dense_4_bias*
Tin
2*
Tout
2*
_collective_manager_ids
 *'
_output_shapes
:���������9*$
_read_only_resource_inputs
*0
config_proto 

CPU

GPU2*0J 8� *M
fHRF
D__inference_dense_4_layer_call_and_return_conditional_losses_1619216�
leaky_re_lu_3/PartitionedCallPartitionedCall(dense_4/StatefulPartitionedCall:output:0*
Tin
2*
Tout
2*
_collective_manager_ids
 *'
_output_shapes
:���������9* 
_read_only_resource_inputs
 *0
config_proto 

CPU

GPU2*0J 8� *S
fNRL
J__inference_leaky_re_lu_3_layer_call_and_return_conditional_losses_1619224�
dense_5/StatefulPartitionedCallStatefulPartitionedCall&leaky_re_lu_3/PartitionedCall:output:0dense_5_dense_5_kerneldense_5_dense_5_bias*
Tin
2*
Tout
2*
_collective_manager_ids
 *'
_output_shapes
:���������y*$
_read_only_resource_inputs
*0
config_proto 

CPU

GPU2*0J 8� *M
fHRF
D__inference_dense_5_layer_call_and_return_conditional_losses_1619235w
IdentityIdentity(dense_5/StatefulPartitionedCall:output:0^NoOp*
T0*'
_output_shapes
:���������y�
NoOpNoOp ^dense_3/StatefulPartitionedCall ^dense_4/StatefulPartitionedCall ^dense_5/StatefulPartitionedCall*
_output_shapes
 "
identityIdentity:output:0*(
_construction_contextkEagerRuntime*2
_input_shapes!
:���������R: : : : : : 2B
dense_3/StatefulPartitionedCalldense_3/StatefulPartitionedCall2B
dense_4/StatefulPartitionedCalldense_4/StatefulPartitionedCall2B
dense_5/StatefulPartitionedCalldense_5/StatefulPartitionedCall:,(
&
_user_specified_namedense_5/bias:.*
(
_user_specified_namedense_5/kernel:,(
&
_user_specified_namedense_4/bias:.*
(
_user_specified_namedense_4/kernel:,(
&
_user_specified_namedense_3/bias:.*
(
_user_specified_namedense_3/kernel:O K
'
_output_shapes
:���������R
 
_user_specified_nameinputs
�

�
D__inference_dense_5_layer_call_and_return_conditional_losses_1619235

inputs6
$matmul_readvariableop_dense_5_kernel:9y1
#biasadd_readvariableop_dense_5_bias:y
identity��BiasAdd/ReadVariableOp�MatMul/ReadVariableOpz
MatMul/ReadVariableOpReadVariableOp$matmul_readvariableop_dense_5_kernel*
_output_shapes

:9y*
dtype0i
MatMulMatMulinputsMatMul/ReadVariableOp:value:0*
T0*'
_output_shapes
:���������yv
BiasAdd/ReadVariableOpReadVariableOp#biasadd_readvariableop_dense_5_bias*
_output_shapes
:y*
dtype0v
BiasAddBiasAddMatMul:product:0BiasAdd/ReadVariableOp:value:0*
T0*'
_output_shapes
:���������y_
IdentityIdentityBiasAdd:output:0^NoOp*
T0*'
_output_shapes
:���������yS
NoOpNoOp^BiasAdd/ReadVariableOp^MatMul/ReadVariableOp*
_output_shapes
 "
identityIdentity:output:0*(
_construction_contextkEagerRuntime**
_input_shapes
:���������9: : 20
BiasAdd/ReadVariableOpBiasAdd/ReadVariableOp2.
MatMul/ReadVariableOpMatMul/ReadVariableOp:,(
&
_user_specified_namedense_5/bias:.*
(
_user_specified_namedense_5/kernel:O K
'
_output_shapes
:���������9
 
_user_specified_nameinputs
�
�
I__inference_sequential_1_layer_call_and_return_conditional_losses_1619414

inputs>
,dense_3_matmul_readvariableop_dense_3_kernel:RF9
+dense_3_biasadd_readvariableop_dense_3_bias:F>
,dense_4_matmul_readvariableop_dense_4_kernel:F99
+dense_4_biasadd_readvariableop_dense_4_bias:9>
,dense_5_matmul_readvariableop_dense_5_kernel:9y9
+dense_5_biasadd_readvariableop_dense_5_bias:y
identity��dense_3/BiasAdd/ReadVariableOp�dense_3/MatMul/ReadVariableOp�dense_4/BiasAdd/ReadVariableOp�dense_4/MatMul/ReadVariableOp�dense_5/BiasAdd/ReadVariableOp�dense_5/MatMul/ReadVariableOp�
dense_3/MatMul/ReadVariableOpReadVariableOp,dense_3_matmul_readvariableop_dense_3_kernel*
_output_shapes

:RF*
dtype0y
dense_3/MatMulMatMulinputs%dense_3/MatMul/ReadVariableOp:value:0*
T0*'
_output_shapes
:���������F�
dense_3/BiasAdd/ReadVariableOpReadVariableOp+dense_3_biasadd_readvariableop_dense_3_bias*
_output_shapes
:F*
dtype0�
dense_3/BiasAddBiasAdddense_3/MatMul:product:0&dense_3/BiasAdd/ReadVariableOp:value:0*
T0*'
_output_shapes
:���������Fw
leaky_re_lu_2/LeakyRelu	LeakyReludense_3/BiasAdd:output:0*'
_output_shapes
:���������F*
alpha%���>�
dense_4/MatMul/ReadVariableOpReadVariableOp,dense_4_matmul_readvariableop_dense_4_kernel*
_output_shapes

:F9*
dtype0�
dense_4/MatMulMatMul%leaky_re_lu_2/LeakyRelu:activations:0%dense_4/MatMul/ReadVariableOp:value:0*
T0*'
_output_shapes
:���������9�
dense_4/BiasAdd/ReadVariableOpReadVariableOp+dense_4_biasadd_readvariableop_dense_4_bias*
_output_shapes
:9*
dtype0�
dense_4/BiasAddBiasAdddense_4/MatMul:product:0&dense_4/BiasAdd/ReadVariableOp:value:0*
T0*'
_output_shapes
:���������9w
leaky_re_lu_3/LeakyRelu	LeakyReludense_4/BiasAdd:output:0*'
_output_shapes
:���������9*
alpha%���>�
dense_5/MatMul/ReadVariableOpReadVariableOp,dense_5_matmul_readvariableop_dense_5_kernel*
_output_shapes

:9y*
dtype0�
dense_5/MatMulMatMul%leaky_re_lu_3/LeakyRelu:activations:0%dense_5/MatMul/ReadVariableOp:value:0*
T0*'
_output_shapes
:���������y�
dense_5/BiasAdd/ReadVariableOpReadVariableOp+dense_5_biasadd_readvariableop_dense_5_bias*
_output_shapes
:y*
dtype0�
dense_5/BiasAddBiasAdddense_5/MatMul:product:0&dense_5/BiasAdd/ReadVariableOp:value:0*
T0*'
_output_shapes
:���������yg
IdentityIdentitydense_5/BiasAdd:output:0^NoOp*
T0*'
_output_shapes
:���������y�
NoOpNoOp^dense_3/BiasAdd/ReadVariableOp^dense_3/MatMul/ReadVariableOp^dense_4/BiasAdd/ReadVariableOp^dense_4/MatMul/ReadVariableOp^dense_5/BiasAdd/ReadVariableOp^dense_5/MatMul/ReadVariableOp*
_output_shapes
 "
identityIdentity:output:0*(
_construction_contextkEagerRuntime*2
_input_shapes!
:���������R: : : : : : 2@
dense_3/BiasAdd/ReadVariableOpdense_3/BiasAdd/ReadVariableOp2>
dense_3/MatMul/ReadVariableOpdense_3/MatMul/ReadVariableOp2@
dense_4/BiasAdd/ReadVariableOpdense_4/BiasAdd/ReadVariableOp2>
dense_4/MatMul/ReadVariableOpdense_4/MatMul/ReadVariableOp2@
dense_5/BiasAdd/ReadVariableOpdense_5/BiasAdd/ReadVariableOp2>
dense_5/MatMul/ReadVariableOpdense_5/MatMul/ReadVariableOp:,(
&
_user_specified_namedense_5/bias:.*
(
_user_specified_namedense_5/kernel:,(
&
_user_specified_namedense_4/bias:.*
(
_user_specified_namedense_4/kernel:,(
&
_user_specified_namedense_3/bias:.*
(
_user_specified_namedense_3/kernel:O K
'
_output_shapes
:���������R
 
_user_specified_nameinputs
�
f
J__inference_leaky_re_lu_3_layer_call_and_return_conditional_losses_1619224

inputs
identityW
	LeakyRelu	LeakyReluinputs*'
_output_shapes
:���������9*
alpha%���>_
IdentityIdentityLeakyRelu:activations:0*
T0*'
_output_shapes
:���������9"
identityIdentity:output:0*(
_construction_contextkEagerRuntime*&
_input_shapes
:���������9:O K
'
_output_shapes
:���������9
 
_user_specified_nameinputs
�

�
D__inference_dense_4_layer_call_and_return_conditional_losses_1619216

inputs6
$matmul_readvariableop_dense_4_kernel:F91
#biasadd_readvariableop_dense_4_bias:9
identity��BiasAdd/ReadVariableOp�MatMul/ReadVariableOpz
MatMul/ReadVariableOpReadVariableOp$matmul_readvariableop_dense_4_kernel*
_output_shapes

:F9*
dtype0i
MatMulMatMulinputsMatMul/ReadVariableOp:value:0*
T0*'
_output_shapes
:���������9v
BiasAdd/ReadVariableOpReadVariableOp#biasadd_readvariableop_dense_4_bias*
_output_shapes
:9*
dtype0v
BiasAddBiasAddMatMul:product:0BiasAdd/ReadVariableOp:value:0*
T0*'
_output_shapes
:���������9_
IdentityIdentityBiasAdd:output:0^NoOp*
T0*'
_output_shapes
:���������9S
NoOpNoOp^BiasAdd/ReadVariableOp^MatMul/ReadVariableOp*
_output_shapes
 "
identityIdentity:output:0*(
_construction_contextkEagerRuntime**
_input_shapes
:���������F: : 20
BiasAdd/ReadVariableOpBiasAdd/ReadVariableOp2.
MatMul/ReadVariableOpMatMul/ReadVariableOp:,(
&
_user_specified_namedense_4/bias:.*
(
_user_specified_namedense_4/kernel:O K
'
_output_shapes
:���������F
 
_user_specified_nameinputs
�
�
)__inference_dense_3_layer_call_fn_1619445

inputs 
dense_3_kernel:RF
dense_3_bias:F
identity��StatefulPartitionedCall�
StatefulPartitionedCallStatefulPartitionedCallinputsdense_3_kerneldense_3_bias*
Tin
2*
Tout
2*
_collective_manager_ids
 *'
_output_shapes
:���������F*$
_read_only_resource_inputs
*0
config_proto 

CPU

GPU2*0J 8� *M
fHRF
D__inference_dense_3_layer_call_and_return_conditional_losses_1619197o
IdentityIdentity StatefulPartitionedCall:output:0^NoOp*
T0*'
_output_shapes
:���������F<
NoOpNoOp^StatefulPartitionedCall*
_output_shapes
 "
identityIdentity:output:0*(
_construction_contextkEagerRuntime**
_input_shapes
:���������R: : 22
StatefulPartitionedCallStatefulPartitionedCall:,(
&
_user_specified_namedense_3/bias:.*
(
_user_specified_namedense_3/kernel:O K
'
_output_shapes
:���������R
 
_user_specified_nameinputs
�
�
I__inference_sequential_1_layer_call_and_return_conditional_losses_1619255
dense_3_input(
dense_3_dense_3_kernel:RF"
dense_3_dense_3_bias:F(
dense_4_dense_4_kernel:F9"
dense_4_dense_4_bias:9(
dense_5_dense_5_kernel:9y"
dense_5_dense_5_bias:y
identity��dense_3/StatefulPartitionedCall�dense_4/StatefulPartitionedCall�dense_5/StatefulPartitionedCall�
dense_3/StatefulPartitionedCallStatefulPartitionedCalldense_3_inputdense_3_dense_3_kerneldense_3_dense_3_bias*
Tin
2*
Tout
2*
_collective_manager_ids
 *'
_output_shapes
:���������F*$
_read_only_resource_inputs
*0
config_proto 

CPU

GPU2*0J 8� *M
fHRF
D__inference_dense_3_layer_call_and_return_conditional_losses_1619197�
leaky_re_lu_2/PartitionedCallPartitionedCall(dense_3/StatefulPartitionedCall:output:0*
Tin
2*
Tout
2*
_collective_manager_ids
 *'
_output_shapes
:���������F* 
_read_only_resource_inputs
 *0
config_proto 

CPU

GPU2*0J 8� *S
fNRL
J__inference_leaky_re_lu_2_layer_call_and_return_conditional_losses_1619205�
dense_4/StatefulPartitionedCallStatefulPartitionedCall&leaky_re_lu_2/PartitionedCall:output:0dense_4_dense_4_kerneldense_4_dense_4_bias*
Tin
2*
Tout
2*
_collective_manager_ids
 *'
_output_shapes
:���������9*$
_read_only_resource_inputs
*0
config_proto 

CPU

GPU2*0J 8� *M
fHRF
D__inference_dense_4_layer_call_and_return_conditional_losses_1619216�
leaky_re_lu_3/PartitionedCallPartitionedCall(dense_4/StatefulPartitionedCall:output:0*
Tin
2*
Tout
2*
_collective_manager_ids
 *'
_output_shapes
:���������9* 
_read_only_resource_inputs
 *0
config_proto 

CPU

GPU2*0J 8� *S
fNRL
J__inference_leaky_re_lu_3_layer_call_and_return_conditional_losses_1619224�
dense_5/StatefulPartitionedCallStatefulPartitionedCall&leaky_re_lu_3/PartitionedCall:output:0dense_5_dense_5_kerneldense_5_dense_5_bias*
Tin
2*
Tout
2*
_collective_manager_ids
 *'
_output_shapes
:���������y*$
_read_only_resource_inputs
*0
config_proto 

CPU

GPU2*0J 8� *M
fHRF
D__inference_dense_5_layer_call_and_return_conditional_losses_1619235w
IdentityIdentity(dense_5/StatefulPartitionedCall:output:0^NoOp*
T0*'
_output_shapes
:���������y�
NoOpNoOp ^dense_3/StatefulPartitionedCall ^dense_4/StatefulPartitionedCall ^dense_5/StatefulPartitionedCall*
_output_shapes
 "
identityIdentity:output:0*(
_construction_contextkEagerRuntime*2
_input_shapes!
:���������R: : : : : : 2B
dense_3/StatefulPartitionedCalldense_3/StatefulPartitionedCall2B
dense_4/StatefulPartitionedCalldense_4/StatefulPartitionedCall2B
dense_5/StatefulPartitionedCalldense_5/StatefulPartitionedCall:,(
&
_user_specified_namedense_5/bias:.*
(
_user_specified_namedense_5/kernel:,(
&
_user_specified_namedense_4/bias:.*
(
_user_specified_namedense_4/kernel:,(
&
_user_specified_namedense_3/bias:.*
(
_user_specified_namedense_3/kernel:V R
'
_output_shapes
:���������R
'
_user_specified_namedense_3_input
�
K
/__inference_leaky_re_lu_2_layer_call_fn_1619460

inputs
identity�
PartitionedCallPartitionedCallinputs*
Tin
2*
Tout
2*
_collective_manager_ids
 *'
_output_shapes
:���������F* 
_read_only_resource_inputs
 *0
config_proto 

CPU

GPU2*0J 8� *S
fNRL
J__inference_leaky_re_lu_2_layer_call_and_return_conditional_losses_1619205`
IdentityIdentityPartitionedCall:output:0*
T0*'
_output_shapes
:���������F"
identityIdentity:output:0*(
_construction_contextkEagerRuntime*&
_input_shapes
:���������F:O K
'
_output_shapes
:���������F
 
_user_specified_nameinputs"�L
saver_filename:0StatefulPartitionedCall_1:0StatefulPartitionedCall_28"
saved_model_main_op

NoOp*>
__saved_model_init_op%#
__saved_model_init_op

NoOp*�
serving_default�
G
dense_3_input6
serving_default_dense_3_input:0���������R;
dense_50
StatefulPartitionedCall:0���������ytensorflow/serving/predict:��
�
layer_with_weights-0
layer-0
layer-1
layer_with_weights-1
layer-2
layer-3
layer_with_weights-2
layer-4
	variables
trainable_variables
regularization_losses
		keras_api

__call__
*&call_and_return_all_conditional_losses
_default_save_signature
	optimizer

signatures"
_tf_keras_sequential
�
	variables
trainable_variables
regularization_losses
	keras_api
__call__
*&call_and_return_all_conditional_losses

kernel
bias"
_tf_keras_layer
�
	variables
trainable_variables
regularization_losses
	keras_api
__call__
*&call_and_return_all_conditional_losses"
_tf_keras_layer
�
	variables
trainable_variables
regularization_losses
 	keras_api
!__call__
*"&call_and_return_all_conditional_losses

#kernel
$bias"
_tf_keras_layer
�
%	variables
&trainable_variables
'regularization_losses
(	keras_api
)__call__
**&call_and_return_all_conditional_losses"
_tf_keras_layer
�
+	variables
,trainable_variables
-regularization_losses
.	keras_api
/__call__
*0&call_and_return_all_conditional_losses

1kernel
2bias"
_tf_keras_layer
J
0
1
#2
$3
14
25"
trackable_list_wrapper
J
0
1
#2
$3
14
25"
trackable_list_wrapper
 "
trackable_list_wrapper
�
3non_trainable_variables

4layers
5metrics
6layer_regularization_losses
7layer_metrics
	variables
trainable_variables
regularization_losses

__call__
_default_save_signature
*&call_and_return_all_conditional_losses
&"call_and_return_conditional_losses"
_generic_user_object
�
8trace_0
9trace_12�
.__inference_sequential_1_layer_call_fn_1619281
.__inference_sequential_1_layer_call_fn_1619307�
���
FullArgSpec)
args!�
jinputs

jtraining
jmask
varargs
 
varkw
 
defaults�
p 

 

kwonlyargs� 
kwonlydefaults
 
annotations� *
 z8trace_0z9trace_1
�
:trace_0
;trace_1
<trace_2
=trace_32�
I__inference_sequential_1_layer_call_and_return_conditional_losses_1619240
I__inference_sequential_1_layer_call_and_return_conditional_losses_1619255
I__inference_sequential_1_layer_call_and_return_conditional_losses_1619414
I__inference_sequential_1_layer_call_and_return_conditional_losses_1619438�
���
FullArgSpec)
args!�
jinputs

jtraining
jmask
varargs
 
varkw
 
defaults�
p 

 

kwonlyargs� 
kwonlydefaults
 
annotations� *
 z:trace_0z;trace_1z<trace_2z=trace_3
�B�
"__inference__wrapped_model_1619185dense_3_input"�
���
FullArgSpec
args�

jargs_0
varargs
 
varkw
 
defaults
 

kwonlyargs� 
kwonlydefaults
 
annotations� *
 
�
>iter

?beta_1

@beta_2
	Adecay
Blearning_ratemmmn#mo$mp1mq2mrvsvt#vu$vv1vw2vx"
	optimizer
,
Cserving_default"
signature_map
.
0
1"
trackable_list_wrapper
.
0
1"
trackable_list_wrapper
 "
trackable_list_wrapper
�
Dnon_trainable_variables

Elayers
Fmetrics
Glayer_regularization_losses
Hlayer_metrics
	variables
trainable_variables
regularization_losses
__call__
*&call_and_return_all_conditional_losses
&"call_and_return_conditional_losses"
_generic_user_object
�
Itrace_02�
)__inference_dense_3_layer_call_fn_1619445�
���
FullArgSpec
args�

jinputs
varargs
 
varkw
 
defaults
 

kwonlyargs� 
kwonlydefaults
 
annotations� *
 zItrace_0
�
Jtrace_02�
D__inference_dense_3_layer_call_and_return_conditional_losses_1619455�
���
FullArgSpec
args�

jinputs
varargs
 
varkw
 
defaults
 

kwonlyargs� 
kwonlydefaults
 
annotations� *
 zJtrace_0
 :RF2dense_3/kernel
:F2dense_3/bias
 "
trackable_list_wrapper
 "
trackable_list_wrapper
 "
trackable_list_wrapper
�
Knon_trainable_variables

Llayers
Mmetrics
Nlayer_regularization_losses
Olayer_metrics
	variables
trainable_variables
regularization_losses
__call__
*&call_and_return_all_conditional_losses
&"call_and_return_conditional_losses"
_generic_user_object
�
Ptrace_02�
/__inference_leaky_re_lu_2_layer_call_fn_1619460�
���
FullArgSpec
args�

jinputs
varargs
 
varkw
 
defaults
 

kwonlyargs� 
kwonlydefaults
 
annotations� *
 zPtrace_0
�
Qtrace_02�
J__inference_leaky_re_lu_2_layer_call_and_return_conditional_losses_1619465�
���
FullArgSpec
args�

jinputs
varargs
 
varkw
 
defaults
 

kwonlyargs� 
kwonlydefaults
 
annotations� *
 zQtrace_0
.
#0
$1"
trackable_list_wrapper
.
#0
$1"
trackable_list_wrapper
 "
trackable_list_wrapper
�
Rnon_trainable_variables

Slayers
Tmetrics
Ulayer_regularization_losses
Vlayer_metrics
	variables
trainable_variables
regularization_losses
!__call__
*"&call_and_return_all_conditional_losses
&""call_and_return_conditional_losses"
_generic_user_object
�
Wtrace_02�
)__inference_dense_4_layer_call_fn_1619472�
���
FullArgSpec
args�

jinputs
varargs
 
varkw
 
defaults
 

kwonlyargs� 
kwonlydefaults
 
annotations� *
 zWtrace_0
�
Xtrace_02�
D__inference_dense_4_layer_call_and_return_conditional_losses_1619482�
���
FullArgSpec
args�

jinputs
varargs
 
varkw
 
defaults
 

kwonlyargs� 
kwonlydefaults
 
annotations� *
 zXtrace_0
 :F92dense_4/kernel
:92dense_4/bias
 "
trackable_list_wrapper
 "
trackable_list_wrapper
 "
trackable_list_wrapper
�
Ynon_trainable_variables

Zlayers
[metrics
\layer_regularization_losses
]layer_metrics
%	variables
&trainable_variables
'regularization_losses
)__call__
**&call_and_return_all_conditional_losses
&*"call_and_return_conditional_losses"
_generic_user_object
�
^trace_02�
/__inference_leaky_re_lu_3_layer_call_fn_1619487�
���
FullArgSpec
args�

jinputs
varargs
 
varkw
 
defaults
 

kwonlyargs� 
kwonlydefaults
 
annotations� *
 z^trace_0
�
_trace_02�
J__inference_leaky_re_lu_3_layer_call_and_return_conditional_losses_1619492�
���
FullArgSpec
args�

jinputs
varargs
 
varkw
 
defaults
 

kwonlyargs� 
kwonlydefaults
 
annotations� *
 z_trace_0
.
10
21"
trackable_list_wrapper
.
10
21"
trackable_list_wrapper
 "
trackable_list_wrapper
�
`non_trainable_variables

alayers
bmetrics
clayer_regularization_losses
dlayer_metrics
+	variables
,trainable_variables
-regularization_losses
/__call__
*0&call_and_return_all_conditional_losses
&0"call_and_return_conditional_losses"
_generic_user_object
�
etrace_02�
)__inference_dense_5_layer_call_fn_1619499�
���
FullArgSpec
args�

jinputs
varargs
 
varkw
 
defaults
 

kwonlyargs� 
kwonlydefaults
 
annotations� *
 zetrace_0
�
ftrace_02�
D__inference_dense_5_layer_call_and_return_conditional_losses_1619509�
���
FullArgSpec
args�

jinputs
varargs
 
varkw
 
defaults
 

kwonlyargs� 
kwonlydefaults
 
annotations� *
 zftrace_0
 :9y2dense_5/kernel
:y2dense_5/bias
 "
trackable_list_wrapper
C
0
1
2
3
4"
trackable_list_wrapper
'
g0"
trackable_list_wrapper
 "
trackable_list_wrapper
 "
trackable_dict_wrapper
�B�
.__inference_sequential_1_layer_call_fn_1619281dense_3_input"�
���
FullArgSpec)
args!�
jinputs

jtraining
jmask
varargs
 
varkw
 
defaults
 

kwonlyargs� 
kwonlydefaults
 
annotations� *
 
�B�
.__inference_sequential_1_layer_call_fn_1619307dense_3_input"�
���
FullArgSpec)
args!�
jinputs

jtraining
jmask
varargs
 
varkw
 
defaults
 

kwonlyargs� 
kwonlydefaults
 
annotations� *
 
�B�
I__inference_sequential_1_layer_call_and_return_conditional_losses_1619240dense_3_input"�
���
FullArgSpec)
args!�
jinputs

jtraining
jmask
varargs
 
varkw
 
defaults
 

kwonlyargs� 
kwonlydefaults
 
annotations� *
 
�B�
I__inference_sequential_1_layer_call_and_return_conditional_losses_1619255dense_3_input"�
���
FullArgSpec)
args!�
jinputs

jtraining
jmask
varargs
 
varkw
 
defaults
 

kwonlyargs� 
kwonlydefaults
 
annotations� *
 
�B�
I__inference_sequential_1_layer_call_and_return_conditional_losses_1619414inputs"�
���
FullArgSpec)
args!�
jinputs

jtraining
jmask
varargs
 
varkw
 
defaults
 

kwonlyargs� 
kwonlydefaults
 
annotations� *
 
�B�
I__inference_sequential_1_layer_call_and_return_conditional_losses_1619438inputs"�
���
FullArgSpec)
args!�
jinputs

jtraining
jmask
varargs
 
varkw
 
defaults
 

kwonlyargs� 
kwonlydefaults
 
annotations� *
 
:	 (2training/Adam/iter
: (2training/Adam/beta_1
: (2training/Adam/beta_2
: (2training/Adam/decay
%:# (2training/Adam/learning_rate
�B�
%__inference_signature_wrapper_1619390dense_3_input"�
���
FullArgSpec
args� 
varargs
 
varkw
 
defaults
 "

kwonlyargs�
jdense_3_input
kwonlydefaults
 
annotations� *
 
 "
trackable_list_wrapper
 "
trackable_list_wrapper
 "
trackable_list_wrapper
 "
trackable_list_wrapper
 "
trackable_dict_wrapper
�B�
)__inference_dense_3_layer_call_fn_1619445inputs"�
���
FullArgSpec
args�

jinputs
varargs
 
varkw
 
defaults
 

kwonlyargs� 
kwonlydefaults
 
annotations� *
 
�B�
D__inference_dense_3_layer_call_and_return_conditional_losses_1619455inputs"�
���
FullArgSpec
args�

jinputs
varargs
 
varkw
 
defaults
 

kwonlyargs� 
kwonlydefaults
 
annotations� *
 
 "
trackable_list_wrapper
 "
trackable_list_wrapper
 "
trackable_list_wrapper
 "
trackable_list_wrapper
 "
trackable_dict_wrapper
�B�
/__inference_leaky_re_lu_2_layer_call_fn_1619460inputs"�
���
FullArgSpec
args�

jinputs
varargs
 
varkw
 
defaults
 

kwonlyargs� 
kwonlydefaults
 
annotations� *
 
�B�
J__inference_leaky_re_lu_2_layer_call_and_return_conditional_losses_1619465inputs"�
���
FullArgSpec
args�

jinputs
varargs
 
varkw
 
defaults
 

kwonlyargs� 
kwonlydefaults
 
annotations� *
 
 "
trackable_list_wrapper
 "
trackable_list_wrapper
 "
trackable_list_wrapper
 "
trackable_list_wrapper
 "
trackable_dict_wrapper
�B�
)__inference_dense_4_layer_call_fn_1619472inputs"�
���
FullArgSpec
args�

jinputs
varargs
 
varkw
 
defaults
 

kwonlyargs� 
kwonlydefaults
 
annotations� *
 
�B�
D__inference_dense_4_layer_call_and_return_conditional_losses_1619482inputs"�
���
FullArgSpec
args�

jinputs
varargs
 
varkw
 
defaults
 

kwonlyargs� 
kwonlydefaults
 
annotations� *
 
 "
trackable_list_wrapper
 "
trackable_list_wrapper
 "
trackable_list_wrapper
 "
trackable_list_wrapper
 "
trackable_dict_wrapper
�B�
/__inference_leaky_re_lu_3_layer_call_fn_1619487inputs"�
���
FullArgSpec
args�

jinputs
varargs
 
varkw
 
defaults
 

kwonlyargs� 
kwonlydefaults
 
annotations� *
 
�B�
J__inference_leaky_re_lu_3_layer_call_and_return_conditional_losses_1619492inputs"�
���
FullArgSpec
args�

jinputs
varargs
 
varkw
 
defaults
 

kwonlyargs� 
kwonlydefaults
 
annotations� *
 
 "
trackable_list_wrapper
 "
trackable_list_wrapper
 "
trackable_list_wrapper
 "
trackable_list_wrapper
 "
trackable_dict_wrapper
�B�
)__inference_dense_5_layer_call_fn_1619499inputs"�
���
FullArgSpec
args�

jinputs
varargs
 
varkw
 
defaults
 

kwonlyargs� 
kwonlydefaults
 
annotations� *
 
�B�
D__inference_dense_5_layer_call_and_return_conditional_losses_1619509inputs"�
���
FullArgSpec
args�

jinputs
varargs
 
varkw
 
defaults
 

kwonlyargs� 
kwonlydefaults
 
annotations� *
 
^
h	variables
i	keras_api
	jtotal
	kcount
l
_fn_kwargs"
_tf_keras_metric
.
j0
k1"
trackable_list_wrapper
-
h	variables"
_generic_user_object
:  (2total_1
:  (2count_1
 "
trackable_dict_wrapper
.:,RF2training/Adam/dense_3/kernel/m
(:&F2training/Adam/dense_3/bias/m
.:,F92training/Adam/dense_4/kernel/m
(:&92training/Adam/dense_4/bias/m
.:,9y2training/Adam/dense_5/kernel/m
(:&y2training/Adam/dense_5/bias/m
.:,RF2training/Adam/dense_3/kernel/v
(:&F2training/Adam/dense_3/bias/v
.:,F92training/Adam/dense_4/kernel/v
(:&92training/Adam/dense_4/bias/v
.:,9y2training/Adam/dense_5/kernel/v
(:&y2training/Adam/dense_5/bias/v�
"__inference__wrapped_model_1619185s#$126�3
,�)
'�$
dense_3_input���������R
� "1�.
,
dense_5!�
dense_5���������y�
D__inference_dense_3_layer_call_and_return_conditional_losses_1619455c/�,
%�"
 �
inputs���������R
� ",�)
"�
tensor_0���������F
� �
)__inference_dense_3_layer_call_fn_1619445X/�,
%�"
 �
inputs���������R
� "!�
unknown���������F�
D__inference_dense_4_layer_call_and_return_conditional_losses_1619482c#$/�,
%�"
 �
inputs���������F
� ",�)
"�
tensor_0���������9
� �
)__inference_dense_4_layer_call_fn_1619472X#$/�,
%�"
 �
inputs���������F
� "!�
unknown���������9�
D__inference_dense_5_layer_call_and_return_conditional_losses_1619509c12/�,
%�"
 �
inputs���������9
� ",�)
"�
tensor_0���������y
� �
)__inference_dense_5_layer_call_fn_1619499X12/�,
%�"
 �
inputs���������9
� "!�
unknown���������y�
J__inference_leaky_re_lu_2_layer_call_and_return_conditional_losses_1619465_/�,
%�"
 �
inputs���������F
� ",�)
"�
tensor_0���������F
� �
/__inference_leaky_re_lu_2_layer_call_fn_1619460T/�,
%�"
 �
inputs���������F
� "!�
unknown���������F�
J__inference_leaky_re_lu_3_layer_call_and_return_conditional_losses_1619492_/�,
%�"
 �
inputs���������9
� ",�)
"�
tensor_0���������9
� �
/__inference_leaky_re_lu_3_layer_call_fn_1619487T/�,
%�"
 �
inputs���������9
� "!�
unknown���������9�
I__inference_sequential_1_layer_call_and_return_conditional_losses_1619240v#$12>�;
4�1
'�$
dense_3_input���������R
p

 
� ",�)
"�
tensor_0���������y
� �
I__inference_sequential_1_layer_call_and_return_conditional_losses_1619255v#$12>�;
4�1
'�$
dense_3_input���������R
p 

 
� ",�)
"�
tensor_0���������y
� �
I__inference_sequential_1_layer_call_and_return_conditional_losses_1619414o#$127�4
-�*
 �
inputs���������R
p

 
� ",�)
"�
tensor_0���������y
� �
I__inference_sequential_1_layer_call_and_return_conditional_losses_1619438o#$127�4
-�*
 �
inputs���������R
p 

 
� ",�)
"�
tensor_0���������y
� �
.__inference_sequential_1_layer_call_fn_1619281k#$12>�;
4�1
'�$
dense_3_input���������R
p

 
� "!�
unknown���������y�
.__inference_sequential_1_layer_call_fn_1619307k#$12>�;
4�1
'�$
dense_3_input���������R
p 

 
� "!�
unknown���������y�
%__inference_signature_wrapper_1619390�#$12G�D
� 
=�:
8
dense_3_input'�$
dense_3_input���������R"1�.
,
dense_5!�
dense_5���������y