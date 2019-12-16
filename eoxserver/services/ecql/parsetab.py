
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'condition_or_emptyleftEQNEleftGTGELTLEleftPLUSMINUSleftTIMESDIVIDENOT AND OR BETWEEN LIKE ILIKE IN IS NULL BEFORE AFTER DURING INTERSECTS DISJOINT CONTAINS WITHIN TOUCHES CROSSES OVERLAPS EQUALS RELATE DWITHIN BEYOND BBOX feet meters statute miles nautical miles kilometers PLUS MINUS TIMES DIVIDE LT LE GT GE EQ NE LPAREN RPAREN LBRACKET RBRACKET COMMA GEOMETRY ENVELOPE UNITS ATTRIBUTE TIME DURATION FLOAT INTEGER QUOTED condition_or_empty : condition\n                               | empty\n         condition : predicate\n                      | condition AND condition\n                      | condition OR condition\n                      | NOT condition\n                      | LPAREN condition RPAREN\n                      | LBRACKET condition RBRACKET\n         predicate : expression EQ expression\n                      | expression NE expression\n                      | expression LT expression\n                      | expression LE expression\n                      | expression GT expression\n                      | expression GE expression\n                      | expression NOT BETWEEN expression AND expression\n                      | expression BETWEEN expression AND expression\n                      | expression NOT LIKE QUOTED\n                      | expression LIKE QUOTED\n                      | expression NOT ILIKE QUOTED\n                      | expression ILIKE QUOTED\n                      | expression NOT IN LPAREN expression_list RPAREN\n                      | expression IN LPAREN expression_list RPAREN\n                      | expression IS NOT NULL\n                      | expression IS NULL\n                      | temporal_predicate\n                      | spatial_predicate\n         temporal_predicate : expression BEFORE TIME\n                               | expression BEFORE OR DURING time_period\n                               | expression DURING time_period\n                               | expression DURING OR AFTER time_period\n                               | expression AFTER TIME\n         time_period : TIME DIVIDE TIME\n                        | TIME DIVIDE DURATION\n                        | DURATION DIVIDE TIME\n         spatial_predicate : INTERSECTS LPAREN expression COMMA expression RPAREN\n                              | DISJOINT LPAREN expression COMMA expression RPAREN\n                              | CONTAINS LPAREN expression COMMA expression RPAREN\n                              | WITHIN LPAREN expression COMMA expression RPAREN\n                              | TOUCHES LPAREN expression COMMA expression RPAREN\n                              | CROSSES LPAREN expression COMMA expression RPAREN\n                              | OVERLAPS LPAREN expression COMMA expression RPAREN\n                              | EQUALS LPAREN expression COMMA expression RPAREN\n                              | RELATE LPAREN expression COMMA expression COMMA QUOTED RPAREN\n                              | DWITHIN LPAREN expression COMMA expression COMMA number COMMA UNITS RPAREN\n                              | BEYOND LPAREN expression COMMA expression COMMA number COMMA UNITS RPAREN\n                              | BBOX LPAREN expression COMMA number COMMA number COMMA number COMMA number COMMA QUOTED RPAREN\n         expression_list : expression_list COMMA expression\n                            | expression\n         expression : expression PLUS expression\n                       | expression MINUS expression\n                       | expression TIMES expression\n                       | expression DIVIDE expression\n                       | LPAREN expression RPAREN\n                       | LBRACKET expression RBRACKET\n                       | GEOMETRY\n                       | ENVELOPE\n                       | attribute\n                       | QUOTED\n                       | INTEGER\n                       | FLOAT\n         number : INTEGER\n                   | FLOAT\n         attribute : ATTRIBUTE\n        empty : '
    
_lr_action_items = {'CROSSES':([0,6,20,28,44,45,],[7,7,7,7,7,7,]),'INTERSECTS':([0,6,20,28,44,45,],[3,3,3,3,3,3,]),'RELATE':([0,6,20,28,44,45,],[11,11,11,11,11,11,]),'WITHIN':([0,6,20,28,44,45,],[14,14,14,14,14,14,]),'LBRACKET':([0,6,20,28,30,31,32,35,36,37,38,39,40,43,44,45,46,47,49,51,52,53,54,55,56,57,60,61,63,68,69,105,114,117,118,119,120,121,122,123,124,126,127,128,129,138,161,164,],[6,6,6,6,68,68,68,68,68,68,68,68,68,68,6,6,68,68,68,68,68,68,68,68,68,68,68,68,68,68,68,68,68,68,68,68,68,68,68,68,68,68,68,68,68,68,68,68,]),'DURATION':([50,130,132,136,],[90,156,90,90,]),'DISJOINT':([0,6,20,28,44,45,],[8,8,8,8,8,8,]),'DURING':([4,12,17,18,25,26,27,29,34,42,74,82,93,97,99,103,108,],[-57,-59,-58,-56,-55,-63,-60,50,50,50,-54,-53,-50,-49,-52,-51,136,]),'NULL':([58,100,],[101,133,]),'MINUS':([4,12,17,18,25,26,27,29,34,42,70,71,72,74,75,76,77,78,79,80,82,83,86,87,88,93,94,95,96,97,98,99,103,104,106,115,116,135,140,141,142,143,144,145,146,147,148,152,153,154,155,177,179,],[-57,-59,-58,-56,-55,-63,-60,51,51,51,51,51,51,-54,51,51,51,51,51,51,-53,51,51,51,51,-50,51,51,51,-49,51,-52,-51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,]),'DWITHIN':([0,6,20,28,44,45,],[10,10,10,10,10,10,]),'LE':([4,12,17,18,25,26,27,29,34,42,74,82,93,97,99,103,],[-57,-59,-58,-56,-55,-63,-60,52,52,52,-54,-53,-50,-49,-52,-51,]),'RPAREN':([2,4,9,12,15,17,18,25,26,27,41,42,48,73,74,81,82,84,85,91,93,94,95,96,97,98,99,101,102,103,104,106,107,109,110,116,133,134,135,137,139,141,142,143,144,145,148,153,154,155,156,157,158,159,160,162,163,165,166,167,168,169,172,175,176,177,178,179,181,185,188,190,191,193,196,197,],[-26,-57,-25,-59,-3,-58,-56,-55,-63,-60,81,82,-6,-8,-54,-7,-53,-4,-5,-29,-50,-12,-10,-11,-49,-13,-52,-24,-20,-51,-14,-9,-27,-18,-31,82,-23,160,-48,-17,-19,165,166,167,168,169,172,175,176,-16,-33,-32,-34,-30,-22,-28,178,-41,-35,-39,-40,-36,-38,-42,-37,-47,-21,-15,185,-43,191,193,-44,-45,197,-46,]),'TIMES':([4,12,17,18,25,26,27,29,34,42,70,71,72,74,75,76,77,78,79,80,82,83,86,87,88,93,94,95,96,97,98,99,103,104,106,115,116,135,140,141,142,143,144,145,146,147,148,152,153,154,155,177,179,],[-57,-59,-58,-56,-55,-63,-60,60,60,60,60,60,60,-54,60,60,60,60,60,60,-53,60,60,60,60,60,60,60,60,60,60,-52,-51,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,]),'NE':([4,12,17,18,25,26,27,29,34,42,74,82,93,97,99,103,],[-57,-59,-58,-56,-55,-63,-60,53,53,53,-54,-53,-50,-49,-52,-51,]),'LT':([4,12,17,18,25,26,27,29,34,42,74,82,93,97,99,103,],[-57,-59,-58,-56,-55,-63,-60,54,54,54,-54,-53,-50,-49,-52,-51,]),'PLUS':([4,12,17,18,25,26,27,29,34,42,70,71,72,74,75,76,77,78,79,80,82,83,86,87,88,93,94,95,96,97,98,99,103,104,106,115,116,135,140,141,142,143,144,145,146,147,148,152,153,154,155,177,179,],[-57,-59,-58,-56,-55,-63,-60,55,55,55,55,55,55,-54,55,55,55,55,55,55,-53,55,55,55,55,-50,55,55,55,-49,55,-52,-51,55,55,55,55,55,55,55,55,55,55,55,55,55,55,55,55,55,55,55,55,]),'INTEGER':([0,6,20,28,30,31,32,35,36,37,38,39,40,43,44,45,46,47,49,51,52,53,54,55,56,57,60,61,63,68,69,105,114,117,118,119,120,121,122,123,124,125,126,127,128,129,138,161,164,170,173,174,186,192,],[12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,151,12,12,12,12,12,12,12,151,151,151,151,151,]),'IN':([4,12,17,18,25,26,27,29,34,42,67,74,82,93,97,99,103,],[-57,-59,-58,-56,-55,-63,-60,62,62,62,112,-54,-53,-50,-49,-52,-51,]),'$end':([0,2,4,9,12,13,15,16,17,18,22,25,26,27,48,73,74,81,82,84,85,91,93,94,95,96,97,98,99,101,102,103,104,106,107,109,110,133,137,139,155,156,157,158,159,160,162,165,166,167,168,169,172,175,176,178,179,185,191,193,197,],[-64,-26,-57,-25,-59,-2,-3,0,-58,-56,-1,-55,-63,-60,-6,-8,-54,-7,-53,-4,-5,-29,-50,-12,-10,-11,-49,-13,-52,-24,-20,-51,-14,-9,-27,-18,-31,-23,-17,-19,-16,-33,-32,-34,-30,-22,-28,-41,-35,-39,-40,-36,-38,-42,-37,-21,-15,-43,-44,-45,-46,]),'OVERLAPS':([0,6,20,28,44,45,],[1,1,1,1,1,1,]),'TOUCHES':([0,6,20,28,44,45,],[5,5,5,5,5,5,]),'GT':([4,12,17,18,25,26,27,29,34,42,74,82,93,97,99,103,],[-57,-59,-58,-56,-55,-63,-60,56,56,56,-54,-53,-50,-49,-52,-51,]),'DIVIDE':([4,12,17,18,25,26,27,29,34,42,70,71,72,74,75,76,77,78,79,80,82,83,86,87,88,89,90,93,94,95,96,97,98,99,103,104,106,115,116,135,140,141,142,143,144,145,146,147,148,152,153,154,155,177,179,],[-57,-59,-58,-56,-55,-63,-60,57,57,57,57,57,57,-54,57,57,57,57,57,57,-53,57,57,57,57,130,131,57,57,57,57,57,57,-52,-51,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,]),'QUOTED':([0,6,20,28,30,31,32,35,36,37,38,39,40,43,44,45,46,47,49,51,52,53,54,55,56,57,59,60,61,63,65,68,69,105,111,113,114,117,118,119,120,121,122,123,124,126,127,128,129,138,161,164,171,195,],[17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,102,17,17,17,109,17,17,17,137,139,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,181,196,]),'IS':([4,12,17,18,25,26,27,29,34,42,74,82,93,97,99,103,],[-57,-59,-58,-56,-55,-63,-60,58,58,58,-54,-53,-50,-49,-52,-51,]),'ENVELOPE':([0,6,20,28,30,31,32,35,36,37,38,39,40,43,44,45,46,47,49,51,52,53,54,55,56,57,60,61,63,68,69,105,114,117,118,119,120,121,122,123,124,126,127,128,129,138,161,164,],[18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,]),'EQUALS':([0,6,20,28,44,45,],[23,23,23,23,23,23,]),'ILIKE':([4,12,17,18,25,26,27,29,34,42,67,74,82,93,97,99,103,],[-57,-59,-58,-56,-55,-63,-60,59,59,59,113,-54,-53,-50,-49,-52,-51,]),'GE':([4,12,17,18,25,26,27,29,34,42,74,82,93,97,99,103,],[-57,-59,-58,-56,-55,-63,-60,61,61,61,-54,-53,-50,-49,-52,-51,]),'BBOX':([0,6,20,28,44,45,],[19,19,19,19,19,19,]),'LPAREN':([0,1,3,5,6,7,8,10,11,14,19,20,21,23,24,28,30,31,32,35,36,37,38,39,40,43,44,45,46,47,49,51,52,53,54,55,56,57,60,61,62,63,68,69,105,112,114,117,118,119,120,121,122,123,124,126,127,128,129,138,161,164,],[20,30,31,32,20,35,36,37,38,39,40,20,43,46,47,20,69,69,69,69,69,69,69,69,69,69,20,20,69,69,69,69,69,69,69,69,69,69,69,69,105,69,69,69,69,138,69,69,69,69,69,69,69,69,69,69,69,69,69,69,69,69,]),'BETWEEN':([4,12,17,18,25,26,27,29,34,42,67,74,82,93,97,99,103,],[-57,-59,-58,-56,-55,-63,-60,49,49,49,114,-54,-53,-50,-49,-52,-51,]),'UNITS':([184,187,],[188,190,]),'BEYOND':([0,6,20,28,44,45,],[21,21,21,21,21,21,]),'EQ':([4,12,17,18,25,26,27,29,34,42,74,82,93,97,99,103,],[-57,-59,-58,-56,-55,-63,-60,63,63,63,-54,-53,-50,-49,-52,-51,]),'BEFORE':([4,12,17,18,25,26,27,29,34,42,74,82,93,97,99,103,],[-57,-59,-58,-56,-55,-63,-60,64,64,64,-54,-53,-50,-49,-52,-51,]),'AND':([2,4,9,12,15,17,18,22,25,26,27,33,41,48,73,74,81,82,84,85,88,91,93,94,95,96,97,98,99,101,102,103,104,106,107,109,110,133,137,139,140,155,156,157,158,159,160,162,165,166,167,168,169,172,175,176,178,179,185,191,193,197,],[-26,-57,-25,-59,-3,-58,-56,44,-55,-63,-60,44,44,44,-8,-54,-7,-53,44,44,129,-29,-50,-12,-10,-11,-49,-13,-52,-24,-20,-51,-14,-9,-27,-18,-31,-23,-17,-19,164,-16,-33,-32,-34,-30,-22,-28,-41,-35,-39,-40,-36,-38,-42,-37,-21,-15,-43,-44,-45,-46,]),'CONTAINS':([0,6,20,28,44,45,],[24,24,24,24,24,24,]),'LIKE':([4,12,17,18,25,26,27,29,34,42,67,74,82,93,97,99,103,],[-57,-59,-58,-56,-55,-63,-60,65,65,65,111,-54,-53,-50,-49,-52,-51,]),'GEOMETRY':([0,6,20,28,30,31,32,35,36,37,38,39,40,43,44,45,46,47,49,51,52,53,54,55,56,57,60,61,63,68,69,105,114,117,118,119,120,121,122,123,124,126,127,128,129,138,161,164,],[25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,]),'ATTRIBUTE':([0,6,20,28,30,31,32,35,36,37,38,39,40,43,44,45,46,47,49,51,52,53,54,55,56,57,60,61,63,68,69,105,114,117,118,119,120,121,122,123,124,126,127,128,129,138,161,164,],[26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,]),'FLOAT':([0,6,20,28,30,31,32,35,36,37,38,39,40,43,44,45,46,47,49,51,52,53,54,55,56,57,60,61,63,68,69,105,114,117,118,119,120,121,122,123,124,125,126,127,128,129,138,161,164,170,173,174,186,192,],[27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,149,27,27,27,27,27,27,27,149,149,149,149,149,]),'AFTER':([4,12,17,18,25,26,27,29,34,42,74,82,92,93,97,99,103,],[-57,-59,-58,-56,-55,-63,-60,66,66,66,-54,-53,132,-50,-49,-52,-51,]),'TIME':([50,64,66,130,131,132,136,],[89,107,110,157,158,89,89,]),'NOT':([0,4,6,12,17,18,20,25,26,27,28,29,34,42,44,45,58,74,82,93,97,99,103,],[28,-57,28,-59,-58,-56,28,-55,-63,-60,28,67,67,67,28,28,100,-54,-53,-50,-49,-52,-51,]),'RBRACKET':([2,4,9,12,15,17,18,25,26,27,33,34,48,73,74,81,82,84,85,91,93,94,95,96,97,98,99,101,102,103,104,106,107,109,110,115,133,137,139,155,156,157,158,159,160,162,165,166,167,168,169,172,175,176,178,179,185,191,193,197,],[-26,-57,-25,-59,-3,-58,-56,-55,-63,-60,73,74,-6,-8,-54,-7,-53,-4,-5,-29,-50,-12,-10,-11,-49,-13,-52,-24,-20,-51,-14,-9,-27,-18,-31,74,-23,-17,-19,-16,-33,-32,-34,-30,-22,-28,-41,-35,-39,-40,-36,-38,-42,-37,-21,-15,-43,-44,-45,-46,]),'COMMA':([4,12,17,18,25,26,27,70,71,72,74,75,76,77,78,79,80,82,83,86,87,93,97,99,103,134,135,146,147,149,150,151,152,163,177,180,182,183,189,194,],[-57,-59,-58,-56,-55,-63,-60,117,118,119,-54,120,121,122,123,124,125,-53,126,127,128,-50,-49,-52,-51,161,-48,170,171,-62,173,-61,174,161,-47,184,186,187,192,195,]),'OR':([2,4,9,12,15,17,18,22,25,26,27,33,41,48,50,64,73,74,81,82,84,85,91,93,94,95,96,97,98,99,101,102,103,104,106,107,109,110,133,137,139,155,156,157,158,159,160,162,165,166,167,168,169,172,175,176,178,179,185,191,193,197,],[-26,-57,-25,-59,-3,-58,-56,45,-55,-63,-60,45,45,45,92,108,-8,-54,-7,-53,45,45,-29,-50,-12,-10,-11,-49,-13,-52,-24,-20,-51,-14,-9,-27,-18,-31,-23,-17,-19,-16,-33,-32,-34,-30,-22,-28,-41,-35,-39,-40,-36,-38,-42,-37,-21,-15,-43,-44,-45,-46,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'predicate':([0,6,20,28,44,45,],[15,15,15,15,15,15,]),'spatial_predicate':([0,6,20,28,44,45,],[2,2,2,2,2,2,]),'condition_or_empty':([0,],[16,]),'attribute':([0,6,20,28,30,31,32,35,36,37,38,39,40,43,44,45,46,47,49,51,52,53,54,55,56,57,60,61,63,68,69,105,114,117,118,119,120,121,122,123,124,126,127,128,129,138,161,164,],[4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,]),'expression_list':([105,138,],[134,163,]),'number':([125,170,173,174,186,192,],[150,180,182,183,189,194,]),'condition':([0,6,20,28,44,45,],[22,33,41,48,84,85,]),'temporal_predicate':([0,6,20,28,44,45,],[9,9,9,9,9,9,]),'expression':([0,6,20,28,30,31,32,35,36,37,38,39,40,43,44,45,46,47,49,51,52,53,54,55,56,57,60,61,63,68,69,105,114,117,118,119,120,121,122,123,124,126,127,128,129,138,161,164,],[29,34,42,29,70,71,72,75,76,77,78,79,80,83,29,29,86,87,88,93,94,95,96,97,98,99,103,104,106,115,116,135,140,141,142,143,144,145,146,147,148,152,153,154,155,135,177,179,]),'time_period':([50,132,136,],[91,159,162,]),'empty':([0,],[13,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> condition_or_empty","S'",1,None,None,None),
  ('condition_or_empty -> condition','condition_or_empty',1,'p_condition_or_empty','parser.py',81),
  ('condition_or_empty -> empty','condition_or_empty',1,'p_condition_or_empty','parser.py',82),
  ('condition -> predicate','condition',1,'p_condition','parser.py',87),
  ('condition -> condition AND condition','condition',3,'p_condition','parser.py',88),
  ('condition -> condition OR condition','condition',3,'p_condition','parser.py',89),
  ('condition -> NOT condition','condition',2,'p_condition','parser.py',90),
  ('condition -> LPAREN condition RPAREN','condition',3,'p_condition','parser.py',91),
  ('condition -> LBRACKET condition RBRACKET','condition',3,'p_condition','parser.py',92),
  ('predicate -> expression EQ expression','predicate',3,'p_predicate','parser.py',105),
  ('predicate -> expression NE expression','predicate',3,'p_predicate','parser.py',106),
  ('predicate -> expression LT expression','predicate',3,'p_predicate','parser.py',107),
  ('predicate -> expression LE expression','predicate',3,'p_predicate','parser.py',108),
  ('predicate -> expression GT expression','predicate',3,'p_predicate','parser.py',109),
  ('predicate -> expression GE expression','predicate',3,'p_predicate','parser.py',110),
  ('predicate -> expression NOT BETWEEN expression AND expression','predicate',6,'p_predicate','parser.py',111),
  ('predicate -> expression BETWEEN expression AND expression','predicate',5,'p_predicate','parser.py',112),
  ('predicate -> expression NOT LIKE QUOTED','predicate',4,'p_predicate','parser.py',113),
  ('predicate -> expression LIKE QUOTED','predicate',3,'p_predicate','parser.py',114),
  ('predicate -> expression NOT ILIKE QUOTED','predicate',4,'p_predicate','parser.py',115),
  ('predicate -> expression ILIKE QUOTED','predicate',3,'p_predicate','parser.py',116),
  ('predicate -> expression NOT IN LPAREN expression_list RPAREN','predicate',6,'p_predicate','parser.py',117),
  ('predicate -> expression IN LPAREN expression_list RPAREN','predicate',5,'p_predicate','parser.py',118),
  ('predicate -> expression IS NOT NULL','predicate',4,'p_predicate','parser.py',119),
  ('predicate -> expression IS NULL','predicate',3,'p_predicate','parser.py',120),
  ('predicate -> temporal_predicate','predicate',1,'p_predicate','parser.py',121),
  ('predicate -> spatial_predicate','predicate',1,'p_predicate','parser.py',122),
  ('temporal_predicate -> expression BEFORE TIME','temporal_predicate',3,'p_temporal_predicate','parser.py',152),
  ('temporal_predicate -> expression BEFORE OR DURING time_period','temporal_predicate',5,'p_temporal_predicate','parser.py',153),
  ('temporal_predicate -> expression DURING time_period','temporal_predicate',3,'p_temporal_predicate','parser.py',154),
  ('temporal_predicate -> expression DURING OR AFTER time_period','temporal_predicate',5,'p_temporal_predicate','parser.py',155),
  ('temporal_predicate -> expression AFTER TIME','temporal_predicate',3,'p_temporal_predicate','parser.py',156),
  ('time_period -> TIME DIVIDE TIME','time_period',3,'p_time_period','parser.py',167),
  ('time_period -> TIME DIVIDE DURATION','time_period',3,'p_time_period','parser.py',168),
  ('time_period -> DURATION DIVIDE TIME','time_period',3,'p_time_period','parser.py',169),
  ('spatial_predicate -> INTERSECTS LPAREN expression COMMA expression RPAREN','spatial_predicate',6,'p_spatial_predicate','parser.py',174),
  ('spatial_predicate -> DISJOINT LPAREN expression COMMA expression RPAREN','spatial_predicate',6,'p_spatial_predicate','parser.py',175),
  ('spatial_predicate -> CONTAINS LPAREN expression COMMA expression RPAREN','spatial_predicate',6,'p_spatial_predicate','parser.py',176),
  ('spatial_predicate -> WITHIN LPAREN expression COMMA expression RPAREN','spatial_predicate',6,'p_spatial_predicate','parser.py',177),
  ('spatial_predicate -> TOUCHES LPAREN expression COMMA expression RPAREN','spatial_predicate',6,'p_spatial_predicate','parser.py',178),
  ('spatial_predicate -> CROSSES LPAREN expression COMMA expression RPAREN','spatial_predicate',6,'p_spatial_predicate','parser.py',179),
  ('spatial_predicate -> OVERLAPS LPAREN expression COMMA expression RPAREN','spatial_predicate',6,'p_spatial_predicate','parser.py',180),
  ('spatial_predicate -> EQUALS LPAREN expression COMMA expression RPAREN','spatial_predicate',6,'p_spatial_predicate','parser.py',181),
  ('spatial_predicate -> RELATE LPAREN expression COMMA expression COMMA QUOTED RPAREN','spatial_predicate',8,'p_spatial_predicate','parser.py',182),
  ('spatial_predicate -> DWITHIN LPAREN expression COMMA expression COMMA number COMMA UNITS RPAREN','spatial_predicate',10,'p_spatial_predicate','parser.py',183),
  ('spatial_predicate -> BEYOND LPAREN expression COMMA expression COMMA number COMMA UNITS RPAREN','spatial_predicate',10,'p_spatial_predicate','parser.py',184),
  ('spatial_predicate -> BBOX LPAREN expression COMMA number COMMA number COMMA number COMMA number COMMA QUOTED RPAREN','spatial_predicate',14,'p_spatial_predicate','parser.py',185),
  ('expression_list -> expression_list COMMA expression','expression_list',3,'p_expression_list','parser.py',203),
  ('expression_list -> expression','expression_list',1,'p_expression_list','parser.py',204),
  ('expression -> expression PLUS expression','expression',3,'p_expression','parser.py',213),
  ('expression -> expression MINUS expression','expression',3,'p_expression','parser.py',214),
  ('expression -> expression TIMES expression','expression',3,'p_expression','parser.py',215),
  ('expression -> expression DIVIDE expression','expression',3,'p_expression','parser.py',216),
  ('expression -> LPAREN expression RPAREN','expression',3,'p_expression','parser.py',217),
  ('expression -> LBRACKET expression RBRACKET','expression',3,'p_expression','parser.py',218),
  ('expression -> GEOMETRY','expression',1,'p_expression','parser.py',219),
  ('expression -> ENVELOPE','expression',1,'p_expression','parser.py',220),
  ('expression -> attribute','expression',1,'p_expression','parser.py',221),
  ('expression -> QUOTED','expression',1,'p_expression','parser.py',222),
  ('expression -> INTEGER','expression',1,'p_expression','parser.py',223),
  ('expression -> FLOAT','expression',1,'p_expression','parser.py',224),
  ('number -> INTEGER','number',1,'p_number','parser.py',241),
  ('number -> FLOAT','number',1,'p_number','parser.py',242),
  ('attribute -> ATTRIBUTE','attribute',1,'p_attribute','parser.py',247),
  ('empty -> <empty>','empty',0,'p_empty','parser.py',252),
]