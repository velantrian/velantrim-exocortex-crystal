"""Offline probe, usable unchanged against base and proposed trees."""
import json, sys, os, tempfile
from pathlib import Path
sys.path.insert(0, sys.argv[1])
root=Path(tempfile.mkdtemp(prefix="crystal-applicability-probe-"))
os.environ.update(VELANTRIM_L3_BACKEND="sqlite", VELANTRIM_L3_PATH=str(root/'l3.db'),
                  VELANTRIM_STORAGE_PROFILE_PATH=str(root/'profile.json'),
                  VELANTRIM_EMBEDDER="hashing", VELANTRIM_GENERATOR="extractive",
                  VELANTRIM_QUEUE_BACKEND="sqlite", VELANTRIM_DEMO_SEED="0")
from core import memory, pipeline
memory.SQLITE_PATH=str(root/'l1.db')

def fact(**extra):
 return dict(fact_id='probe',claim='L ready',source='synthetic-fixture',confidence=1.0,
             epistemic_state='Validated',truth_status='VERIFIED',claim_type='WORLD_FACT',
             source_status='EXTERNAL',restricted=False,primary_object='L',**extra)
now='2026-11-08T10:00:00+01:00'
cases={
 'later_observation': (fact(observed_at='2026-11-08T23:00:00+01:00'),now),
 'expired_interval': (fact(valid_from='2026-11-08T00:00:00+01:00',valid_until='2026-11-08T01:00:00+01:00'),now),
 'invalid_as_of': (fact(observed_at=now),'2026-11-08oops'),
 'today_write_old_event': (fact(observed_at='2026-10-08',recorded_at='2026-11-08'),now),
 'write_only': (fact(recorded_at=now),now),
 'current_without_as_of': (fact(observed_at='2026-10-08'),None),
 'fresh_matching': (fact(observed_at=now),now),
}
foreign=fact(observed_at=now);foreign['primary_object']='L2';foreign['linked_objects']=['L']
cases['linked_no_transfer']=(foreign,now)
unknown=fact(observed_at=now);unknown.pop('primary_object');cases['missing_object_belonging']=(unknown,now)
results={}
for name,(record,as_of) in cases.items():
 out=pipeline.generate_answer(dict(facts=[record],query='What is L status?',asked_object='L',
                                  as_of=as_of,temporal_scope='current'),[])
 results[name]={k:out.get(k) for k in ('answer','error','facts','applicability')}
item=dict(id='stored',text='L ready',source='fixture',confidence=1.0,epistemic_state='Observed',
          primary_object='L2',linked_objects=['L'],status_applies_to=['L'],observed_at=now,recorded_at='2026-11-09')
pipeline.build_facts_pack([item],'probe')
memory._L0.clear()
results['real_store_cache_clear_reload']={'metadata':memory.get_fact('stored')['metadata']}
print(json.dumps(results,ensure_ascii=False,indent=2))
