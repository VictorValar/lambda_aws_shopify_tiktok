function() {
    var items = {
        { dlv - eventModel.items } };
    var contents = items.replace('id', 'content_id');
    contents = items.replace('name', 'content_name');
    contents = items.replace('category', 'content_category');
    console.log('###############################################')
    console.log(contents)
    return contents
}

var contents = items.toString()
contents.replace('id', 'content_id');
contents.replace('name', 'content_name');
contents.replace('category', 'content_category');


​
ttq.track('AddToCart', { content_name: DYNAMIC_PRODUCT_NAME_COMES_HERE, value: DYNAMIC_ORDER_VALUE_COMES_HERE, currency: 'USD', ​ });


for (var i = 0; i < items.length; i++) {
    var item = items[i];
    console.log(item);
}