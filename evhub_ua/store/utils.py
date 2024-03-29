def get_first_image(context):
	try:
		chargersitems = context['items']
	except:
		chargersitems = context

	chargersitems_images = {}

	for item in chargersitems:
		# Отримати всі екземпляри AttachmentAccessories, які відповідають поточному аксесуару
		attachment_chargersitems = item.attachmentchargersitems_set.all()
		# Припускається, що у моделі AttachmentAccessories є ForeignKey до моделі Gallery
		if attachment_chargersitems:
			chargersitems_images[item.slug] = [attachment_chargersitems.first().gallery.images.url]
		else:
			chargersitems_images[item.slug] = None

	return chargersitems_images

def get_all_images(context):
	try:
		chargersitems = context['item']
	except:
		chargersitems = context

	chargersitems_images = {}

	if chargersitems:
		# Отримати всі екземпляри AttachmentAccessories, які відповідають поточному аксесуару
		attachment_chargersitems = chargersitems.attachmentchargersitems_set.all()
		# Припускається, що у моделі AttachmentAccessories є ForeignKey до моделі Gallery
		if attachment_chargersitems:
			chargersitems_images[chargersitems.slug] = [attachment.gallery.images.url for attachment in
														attachment_chargersitems]
		else:
			chargersitems_images[chargersitems.slug] = None

	return chargersitems_images

def get_all_imagesA(context):
	try:
		accessories = context['item']
	except:
		accessories = context

	accessories_images = {}

	if accessories:
		# Отримати всі екземпляри AttachmentAccessories, які відповідають поточному аксесуару
		attachment_accessories = accessories.attachmentaccessories_set.all()
		# Припускається, що у моделі AttachmentAccessories є ForeignKey до моделі Gallery
		if attachment_accessories:
			accessories_images[accessories.slug] = [attachment.gallery.images.url for attachment in
														attachment_accessories]
		else:
			accessories_images[accessories.slug] = None

	return accessories_images

def get_first_imageA(context):
	try:
		accessories = context['items']
	except:
		accessories = context
	accessories_images = {}

	for item in accessories:
		# Отримати всі екземпляри AttachmentAccessories, які відповідають поточному аксесуару
		attachment_accessories = item.attachmentaccessories_set.all()
		# Припускається, що у моделі AttachmentAccessories є ForeignKey до моделі Gallery
		if attachment_accessories:
			accessories_images[item.slug] = [attachment_accessories.first().gallery.images.url]
		else:
			accessories_images[item.slug] = None

	return accessories_images
