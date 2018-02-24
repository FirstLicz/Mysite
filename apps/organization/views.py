from django.shortcuts import render
from django.views.generic import View


from organization.models import CourseOrg,CityDict

# Create your views here.


class OrganzationView(View):

    def get(self,request):
        #所有机构
        all_orgs = CourseOrg.objects.all()
        #所有城市
        all_city = CityDict.objects.all()

        return render(request,'organization/org-list.html',{
            'all_orgs':all_orgs,'all_city':all_city,
        })




