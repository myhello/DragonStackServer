import XenAPI
import provision
import time
import sys
class Xen():
	def __init__(self,url,user,pwd):
		try:
			session = XenAPI.Session(url)
			session.xenapi.login_with_password(user,pwd)
			print "connect xenserver "+url+" success!"
		except Exception, e:
			print "connect xenserver failed for that: "+str(e)

		self.session = session

	def get_template_list(self):
		templates = self.session.xenapi.VM.get_all_records()
		template_list = []
		for tpl in templates:
			#if not 'Production' in templates[tpl]['tags']: continue
			if not templates[tpl]["is_a_template"]: continue
			template_list += [(templates[tpl]['uuid'], templates[tpl]['name_label'])]
		return template_list

	def get_host_list(self):
		hosts = self.session.xenapi.host.get_all_records()
		host_list = []
		for host in hosts:
			host_ref = self.session.xenapi.host.get_by_uuid(hosts[host]['uuid'])
			host_list += [hosts[host]['name_label']]

		return host_list,host_ref

	def vm_list(self):
		try:
			vms = self.session.xenapi.VM.get_all_records()
		except:
			pass
		for vm in vms:
			print vms[vm]['uuid']
			break
		return vms

	def vm_details(self, uuid):
		vm_ref = self.session.xenapi.VM.get_by_uuid(uuid)
		vm_details = self.session.xenapi.VM.get_record(vm_ref)
		return vm_details

	def get_tags(self):
		poolrefs = self.session.xenapi.pool.get_all()
		tags = self.session.xenapi.pool.get_tags(poolrefs[0])
		return tags

	def get_other_config(self):
		poolrefs = self.session.xenapi.pool.get_all()
		other_config = self.session.xenapi.pool.get_other_config(poolrefs[0])
		return other_config

	def find_uuid_by_lable(self,lable):
		try:
			vms = self.session.xenapi.VM.get_all_records()
			uuid = ''
		except:
			pass
		for vm in vms:
			if vms[vm]['name_label'] == lable:
				uuid = vms[vm]['uuid'] 
				break
		return uuid

	def vm_start(self, uuid):
		ref = self.session.xenapi.VM.get_by_uuid(uuid)
		try:
			self.session.xenapi.VM.start(ref, False, True)
			print "start vm success!"
		except:
			print "start vm failed!"

	def vm_stop(self, uuid):
		ref = self.session.xenapi.VM.get_by_uuid(uuid)
		try:
			self.session.xenapi.VM.clean_shutdown(ref)
			#self.session.xenapi.VM.hard_shutdown(ref)
			#self.session.xenapi.Async.VM.clean_shutdown(ref)
			print "stop vm success!"
		except:
			print "stop vm failed!"

	def get_uuid(self,vm_ref):
		vm_details = self.session.xenapi.VM.get_record(vm_ref)
		return vm_details['uuid']

	def vm_destroy(self, uuid):
		# Before destroying the VM, first destroy all the Disks and network interfaces the VM has.
		vm_ref = self.session.xenapi.VM.get_by_uuid(uuid)
		vm_details = self.session.xenapi.VM.get_record(vm_ref)
		
		if vm_details['power_state'] == 'Running':
			self.vm_stop(uuid)
		
		vbds = vm_details['VBDs']
		vifs = vm_details['VIFs']

		# Loop through all the VBDs
		for vbd_ref in vbds:
			# Each VDB contains a VDI and also has to be destroyed
			vbd_records = self.session.xenapi.VBD.get_record(vbd_ref)
			vdi_ref = self.session.xenapi.VBD.get_VDI(vbd_ref)
			try:
				self.session.xenapi.VDI.destroy(vdi_ref)
			except:
				pass

			try:
				self.session.xenapi.VBD.destroy(vbd_ref)
			except:
				pass

		# Loop through all the VIFs
		for vif_ref in vifs:
			try:
				self.session.xenapi.VIF.destroy(vif_ref)
			except:
				pass
		try:
			self.session.xenapi.VM.destroy(vm_ref)
		except:
			pass

     
	def hasTemplate(self,vm_template):
		vms = self.session.xenapi.VM.get_all_records() 

		templates = []
		for vm in vms:
		    record = vms[vm]
		    if record["is_a_template"]:
		        if record["name_label"]==vm_template:
		            templates.append(vm)
		if templates == []:
		    return False
		else:
		    return True

	def freeDeploy(self):
		host,host_ref = self.get_host_list()
		host_metrics = self.session.xenapi.host.get_metrics(host_ref)
		live = self.session.xenapi.host_metrics.get_record(host_metrics)['live']
		free_memory = int(self.session.xenapi.host_metrics.get_record(host_metrics)['memory_free'])

		cpu_info = self.session.xenapi.host.get_cpu_info(host_ref)
		
		pool = self.session.xenapi.pool.get_all()[0]
		SR = self.session.xenapi.pool.get_default_SR(pool)
		
		virtual_allocation = int(self.session.xenapi.SR.get_virtual_allocation(SR))
		physical_size = int(self.session.xenapi.SR.get_physical_size(SR))
	        physical_utilisation = int(self.session.xenapi.SR.get_physical_utilisation(SR))	
		#return live,free_memory,(physical_size-virtual_allocation)
                return live,free_memory,(physical_size-physical_utilisation)


	def vm_template_copy(self,vm_template,vm_name):
		pifs = self.session.xenapi.PIF.get_all_records()
		lowest = None
		for pifRef in pifs.keys():
			if (lowest is None) or (pifs[pifRef]['device'] < pifs[lowest]['device']):
	  			lowest = pifRef
		print "Choosing PIF with device: ", pifs[lowest]['device']

		network = self.session.xenapi.PIF.get_network(lowest)
		print "Chosen PIF is connected to network: ", self.session.xenapi.network.get_name_label(network)

		# List all the VM objects
		vms = self.session.xenapi.VM.get_all_records()

		templates = []
		for vm in vms:
		    record = vms[vm]
		    ty = "VM"
		    if record["is_a_template"]:
		        ty = "Template"
		        if record["name_label"] == vm_template:
		            templates.append(vm)

		print "Choosing a template to clone"
		if templates == []:
		    print "Could not find any templates. Exitting"
		    sys.exit(1)

		template = templates[0]
		print "Installing new VM from the template"
		vm = self.session.xenapi.VM.clone(template, vm_name)
		#print vm
		vm_uuid = self.get_uuid(vm)
		print "  New VM has name: "+vm_name
		print "Creating VIF"
		vif = { 'device': '0',
		        'network': network,
		        'VM': vm,
		        'MAC': "",
		        'MTU': "1500",
		        "qos_algorithm_type": "",
		        "qos_algorithm_params": {},
		        "other_config": {} }
		self.session.xenapi.VIF.create(vif)
		self.session.xenapi.VM.set_PV_args(vm, "noninteractive")
		print "Choosing an SR to instaniate the VM's disks"
		pool = self.session.xenapi.pool.get_all()[0]
		default_sr = self.session.xenapi.pool.get_default_SR(pool)
		default_sr = self.session.xenapi.SR.get_record(default_sr)
		print "Choosing SR: %s (uuid %s)" % (default_sr['name_label'], default_sr['uuid'])
		print "Rewriting the disk provisioning XML"

		ps = provision.ProvisionSpec()
		provision.setProvisionSpec(self.session,vm,ps)

		spec = provision.getProvisionSpec(self.session, vm)
		spec.setSR(default_sr['uuid'])
		#print spec

		provision.setProvisionSpec(self.session, vm, spec)
		print "Asking server to provision storage from the template specification"
		self.session.xenapi.VM.provision(vm)

		return vm_uuid,vm
		print "Starting VM"
		self.session.xenapi.VM.start(vm, False, True)
		print "  VM is booting"

		print "Waiting for the installation to complete"
		# Here we poll because we don't generate events for metrics objects currently

		def read_os_name(vm):
		    vgm = self.session.xenapi.VM.get_guest_metrics(vm)
		    try:
		        os = self.session.xenapi.VM_guest_metrics.get_os_version(vgm)
		        if "name" in os.keys():
		            return os["name"]
		        return None
		    except:
		        return None
		def read_ip_address(vm):
		    vgm = self.session.xenapi.VM.get_guest_metrics(vm)
		    try:
		        os = self.session.xenapi.VM_guest_metrics.get_networks(vgm)
		        if "0/ip" in os.keys():
		            return os["0/ip"]
		        return None
		    except:
		        return None

		while read_os_name(vm) == None: time.sleep(1)
		print "Reported OS name: ", read_os_name(vm)
		while read_ip_address(vm) == None: time.sleep(1)
		print "Reported IP: ", read_ip_address(vm)

		self.session.xenapi.session.logout()

	def read_ip_address(self,vm_ref):
	    vgm = self.session.xenapi.VM.get_guest_metrics(vm_ref)
	    try:
	        os = self.session.xenapi.VM_guest_metrics.get_networks(vgm)
	        if "0/ip" in os.keys():
	            return os["0/ip"]
	        return None
	    except:
	        return None


	def stop_vm(session, vm, force):
	    current_state = session.xenapi.VM.get_power_state(vm)
	    requested_state = 'stop'

	    if _is_operation_allowed(session, vm, "VM", "clean_shutdown"):
	        if validate_vm_state(current_state, requested_state, force):

	            if not force:
	                session.xenapi.Async.VM.clean_shutdown(vm)
	                print "VM successfully soft shutdown"
	            else:
	                session.xenapi.VM.hard_shutdown(vm)
	                print "VM successfully hard shutdown"
	    else:
	        print "Clean shutdown is not allowed on VM, Attempting a hard shutdown"
	        session.xenapi.VM.hard_shutdown(vm)
	        print "VM successfully hard shutdown"

	def vm_update(self, uuid, fields):
		memory        = int(fields['mem_size'])*1024*1024*1024
		cpu_cores     = int(fields['cpu_cores'])
		description   = fields['description']
		vm_ref        = self.session.xenapi.VM.get_by_uuid(uuid)
		cur_cpu_cores = int(self.session.xenapi.VM.get_VCPUs_max(vm_ref))

		tags          = fields['tags']
		#print fields

		self.session.xenapi.VM.set_tags(vm_ref, tags)

		other_data = {}
		if fields['backup'] is True:
			other_data['XenCenter.CustomFields.backup'] = '1'
		else:
			other_data['XenCenter.CustomFields.backup'] = '0'

		for item in fields:
			if 'customfield' not in item: continue
			field = str(item.split('.')[1])
			other_data['XenCenter.CustomFields.%s' % field] = str(fields[item])

		self.session.xenapi.VM.set_other_config(vm_ref, other_data)
		self.session.xenapi.VM.set_name_description(vm_ref, description)

		vm_details = self.session.xenapi.VM.get_record(vm_ref)

		if vm_details['power_state'] == 'Running':
			self.vm_stop(uuid)
			time.sleep(10)

			if cur_cpu_cores >= cpu_cores:
				self.session.xenapi.VM.set_VCPUs_at_startup(vm_ref, str(cpu_cores))
				self.session.xenapi.VM.set_VCPUs_max(vm_ref, str(cpu_cores))
			else:
				self.session.xenapi.VM.set_VCPUs_max(vm_ref, str(cpu_cores))
				self.session.xenapi.VM.set_VCPUs_at_startup(vm_ref, str(cpu_cores))

			self.session.xenapi.VM.set_memory_limits(vm_ref, str(memory), str(memory), str(memory),str(memory))
			
			self.vm_start(uuid)
			time.sleep(10)
		else:
			if cur_cpu_cores >= cpu_cores:
				self.session.xenapi.VM.set_VCPUs_at_startup(vm_ref, str(cpu_cores))
				self.session.xenapi.VM.set_VCPUs_max(vm_ref, str(cpu_cores))
			else:
				self.session.xenapi.VM.set_VCPUs_max(vm_ref, str(cpu_cores))
				self.session.xenapi.VM.set_VCPUs_at_startup(vm_ref, str(cpu_cores))

			self.session.xenapi.VM.set_memory_limits(vm_ref, str(memory), str(memory), str(memory),str(memory))
			
			self.vm_start(uuid)
			time.sleep(10)


	def host_details(self, host_ref):
		host_details = self.session.xenapi.host.get_record(host_ref)
		return host_details

	def find_vbds(self,uuid):
		vm_ref = self.session.xenapi.VM.get_by_uuid(uuid)
		vm_details = self.session.xenapi.VM.get_record(vm_ref)
		vbds = vm_details['VBDs']
		return vbds

	def find_vdis(self,vbds):
		for vbd_ref in vbds:
			vbd_records = self.session.xenapi.VBD.get_record(vbd_ref)
			if not vbd_records['type'] == 'Disk': continue
			return vbd_records['VDI']

	def disks_by_vdb(self, vbds):
		data = []
		for vbd_ref in vbds:
			vbd_records = self.session.xenapi.VBD.get_record(vbd_ref)
			if not vbd_records['type'] == 'Disk': continue
			print vbd_records['VDI']
			vdi_records = self.session.xenapi.VDI.get_record(vbd_records['VDI'])
			data += [{
				'name':                 vdi_records["name_label"],
				'size':                 vdi_records["virtual_size"],
				'physical_utilisation': vdi_records["physical_utilisation"],
			}]
		return data

	def update_disk(self,vm_uuid,size):
		vdi = self.find_vdis(self.find_vbds(vm_uuid))
		self.session.xenapi.VDI.resize(vdi,size)

if __name__ == '__main__':
	url = "http://192.168.0.2"
	user = "root"
	pwd = "123456"
	xen = Xen(url,user,pwd)

	fields = {}
	fields['description'] = 'Windows Template777'
	fields['cpu_cores'] = 4
	fields['backup'] = False
	fields['mem_size'] = 6
	List_tags = ['windows','']
	fields['tags'] = List_tags
        
        #print fields
     	size = 80*1024*1024*1024 
        uuid = '04b17d39-7df1-8df0-252e-20563299bb18'
        #xen.update_disk(uuid,str(size))
        #xen.vm_update(uuid,fields)
	#
	print xen.hasTemplate("My Ubuntu Server Template")
