

.PHONY: local online update_presentation

local: .vbox_box_created update_presentation
	cd vagrant/vbox; \
	time vagrant reload --provision

destroy-local:
	cd vagrant/vbox; \
	vagrant destroy -f
	rm .vbox_box_created


.vbox_box_created:
	cd vagrant/vbox; \
	time vagrant up --provider=virtualbox

online: .do_box_created update_presentation
	cd vagrant/do; \
	time vagrant reload --provision

.do_box_created:
	cd vagrant/do; \
	time vagrant up --provider=digitalocean

update_presentation:
	cp presentation.html vagrant/index.html
