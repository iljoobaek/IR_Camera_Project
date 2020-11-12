export PYTHONPATH=$PYTHONPATH:../../models/research/:../../models/research/slim
python create_xml_tf_record.py --type=test
