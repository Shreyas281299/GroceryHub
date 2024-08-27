from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required
from app.models.productModel import ProductModel,SectionModel
from app.forms import searchForm


section_bp = Blueprint('section', __name__)

@section_bp.route("/section", methods=['GET'])
@section_bp.route("/section/<section>", methods=['GET'])
@login_required
def section_view(section=None):
    sectionsData = [sec.sectionValue.capitalize()
                    for sec in SectionModel.query.all()]

    if (section):
        productDataArray = ProductModel.query.filter_by(
            section=section.lower())
        return render_template('sections.html', productDataArray=productDataArray, sections=sectionsData, sectionCategory=section)

    productDataArray = ProductModel.query.all()
    return render_template('sections.html', productDataArray=productDataArray, sections=sectionsData)

@section_bp.route("/search", methods=['GET','POST'])
@section_bp.route("/search/<query>", methods=['GET','POST'])
@login_required
def search(advancedSearch=None):
    print("IN search")
    if advancedSearch:
        advancedSearchForm = searchForm.AdvancedSearch()
        priceFilter = advancedSearchForm.priceFilter.data
        dateFilter = advancedSearchForm.manufacturingDateFilter.data
        if priceFilter:
            searchedProducts = ProductModel.query.filter_by(
                valuePerUnit=priceFilter).all()
            searchedProducts = db.session.query(ProductModel).filter(
                ProductModel.valuePerUnit.between(priceFilter-20, priceFilter+20)).all()
        elif dateFilter:
            my_time = datetime.min.time()
            newDate = datetime.combine(dateFilter, my_time)
            searchedProducts = ProductModel.query.filter_by(
                manufacturingDate=newDate).all()
        newAdvancedSearchForm = searchForm.AdvancedSearch()
        return render_template('search.html', searchedSections=[], searchedProducts=searchedProducts, advancedSearch=newAdvancedSearchForm)

    searchString = request.form['Search']
    if not len(searchString):
        return redirect(url_for('dashboard.dashboard'))
    searchedSection = SectionModel.query.filter(
        SectionModel.sectionKey.like(f"{searchString}%")).all()

    searchedProducts = ProductModel.query.filter(
        ProductModel.productName.like(f"{searchString}%")).all()
    advancedSearchForm = searchForm.AdvancedSearch()
    return render_template('search.html', searchedSections=searchedSection, searchedProducts=searchedProducts, advancedSearch=advancedSearchForm)
