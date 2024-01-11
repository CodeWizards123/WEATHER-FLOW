import yaml
import Logs.Evaluation as Evaluation
from Execute.tcnExecute import tcnExecute

###########################################################

with open('configurations/tcnConfig.yaml', 'r') as file:
    tcnConfig = yaml.safe_load(file)
with open('configurations/sharedConfig.yaml', 'r') as file:
    sharedConfig = yaml.safe_load(file)


tcn_trainer = tcnExecute(sharedConfig, tcnConfig)
tcn_trainer.execute()

Evaluation.TcnEval(tcnConfig, sharedConfig)
