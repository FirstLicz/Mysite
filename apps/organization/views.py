from django.shortcuts import render,HttpResponse
from django.views.generic import View
from django.core.paginator import Paginator
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger


from organization.models import CourseOrg,CityDict
from .forms import UserAskForm


# Create your views here.


class OrganzationView(View):

    def get(self,request):
        #所有机构
        all_orgs = CourseOrg.objects.all()
        #机构的排名
        orgs_order = all_orgs.order_by('-click_nums')[:3]
        #所有城市
        all_city = CityDict.objects.all()
        #筛选城市
        city_id = request.GET.get('city','')
        if city_id:
            all_orgs=all_orgs.filter(city=int(city_id))
        # 筛选类别
        category = request.GET.get('ct', '')
        if category:
            all_orgs = all_orgs.filter(category=category)
        #根据排序选项
        sort_category = request.GET.get('sort','')
        if sort_category:
            all_orgs = all_orgs.order_by('-'+sort_category)
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # Provide Paginator with the request object for complete querystring generation
        p = Paginator(all_orgs,5, request=request)
        orgs = p.page(page)
        return render(request,'organization/org-list.html',{
            'all_orgs':orgs,'all_city':all_city,
            'city_id':city_id,'category':category,'orgs_order':orgs_order,
            'sort_category':sort_category,
        })


class AddUserAskView(View):
    '''
        用户添加咨询
    '''
    def post(self,request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            user_ask = userask_form.save(commit=True)
            return HttpResponse("{'status':'success'}",content_type='application/json')
        else:
            return HttpResponse("{'status':'fail','message': {0}}".format(userask_form.errors))

