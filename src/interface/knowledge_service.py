from knowledge_item import KnowledgeItem

class KnowledgeService:
    def list_knowledge(self):
        knowledge = [
            KnowledgeItem('2020-01-11', 'Learned a new unix command', 'sdgj khdk hsadg /n dsg ladhsg lsdhglds kg/n dsjglk sdahglkads g/n djlg adhslg dh/n'),
            KnowledgeItem('2020-02-13', 'Prototype with SQLite', 'hai lhfasil gah/n asfhl safhlkasf iashf /n ashfilas fhilas fh/n ashfli ashfilas f'),
            KnowledgeItem('2019-05-23', 'VirtualBox init', 'dsgdslhig sdg/n sdigsdi lgudsilgds ug/n sdjgds lgjsdl gds/n sdgiohsdo gdhsiog s'),
            KnowledgeItem('2019-07-01', 'CSS works in mysterious ways', 'sd jfiladsj filadsf /n sdufi sdaufidsa fuidsa f/n sdufop asdufop asdufopsd f/n sadufidso fuiods fuas/n sdufi sdufio sdauf'),
            KnowledgeItem('2020-03-03', 'Markdown 101', 'hdis fhdslk f/n sfhija sfhidlsahklghsghs /n adsjfi dsfids fiodsa f/n dsufi odasufopads fudosp f/n dsaif opdsifo;ds f')
        ]
        return knowledge
