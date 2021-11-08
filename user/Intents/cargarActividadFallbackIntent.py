from lerny.models import *
from lerny.serializers import *
from datetime import datetime


# After upload activities trggered into fallback intent, it should shows you a menu
def cargarActividadFallbackIntent(user_id):
	user_id_obj = User.objects.get(identification=user_id)
	user_lerny = User_Lerny.objects.filter(active=True,user_id=user_id_obj).first()
	lerny_active=user_lerny.lerny_id
	micro_lernys = MicroLerny.objects.filter(lerny=lerny_active).order_by('pk')
	previous_text = "A cual recurso deseas asociar el entregable que acabas de subir?"
	temp = []
	for micro_lerny in micro_lernys:
		resources_microlerny = Resource.objects.filter(microlerny=micro_lerny,resource_type="practical")
		data = ResourceSerializer(resources_microlerny, many=True).data
		i = 0
		
		while(i < len(data)):
			print("IMPRESION LISTAR RECURSOS PRACTICOS: "+ str(data[i]['id'])+") " + data[i]['title'])
			temp.append(
				{
					"subtitle": data[i]['description'],
					"image_url": data[i]['image_url'],
					"title": data[i]['title'],
					"buttons": [
					{
						"payload": "cargar actividad "+str(data[i]['id']),
						"title": "Seleccionar",
						"type": "postback"
					}
					]
				})
			i += 1

	data = {
		"fulfillmentMessages": [
		{
			"text": {
				"text": [
					previous_text
				]
			}
		},
		{
			"payload": {
				"facebook": {
					"attachment": {
						"type": "template",
						"payload": {
							"template_type": "generic",
							"elements": temp
						}
					}
				}
			}
		}]
	}
	return data