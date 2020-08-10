const admin_app = new Vue({
    el: '#admin-app',
    delimiters: ['${', '}'],
    data: {
        id: 0,
        model : "",
        operation : "create",
        name : "",
        username: "",
        password: "",
        url: "",
        is_admin : false,
        users: [],
        categories: [],
        channels: [],
        categ_id: {'id':0,'name':''},
        request_data: null,
        item_to_delete: {'name':''},
        item_to_update: null,
        data_api: [],
    },
    methods:{
        setModelClick(model, operation){
            this.model = model;
            this.operation = operation;
        },
        createClick(){
            params = null;
            self = this;
            
            if(this.model == 'user'){
                params = JSON.stringify({ 
                    "name": this.name, "username": this.username, 
                    "password": this.password, "is_admin": this.is_admin
                });

                $.ajax({
                    url: 'http://127.0.0.1:8000/api/user/create/',
                    contentType: "application/json",
                    dataType: 'json',
                    type: 'POST',
                    data: params,
                    success: function(data){
                        self.users.push(data);
                    },
                    error: function(error) {
                        console.log(error);
                    }
                });
            }
            
            if(this.model == 'category'){
                params = JSON.stringify({ 
                    "name": this.name
                });

                $.ajax({
                    url: 'http://127.0.0.1:8000/api/category/create/',
                    contentType: "application/json",
                    dataType: 'json',
                    type: 'POST',
                    data: params,
                    success: function(data){
                        self.categories.push(data);
                    },
                    error: function(error) {
                        console.log(error);
                    }
                });
            }
            
            if(this.model == 'channel'){
                categ_id = this.categ_id.split('-');
                categ_id = categ_id[0]

                params = JSON.stringify({ 
                    "name": this.name, "url": this.url, "category_id": categ_id
                });

                $.ajax({
                    url: 'http://127.0.0.1:8000/api/channel/create/',
                    contentType: "application/json",
                    dataType: 'json',
                    type: 'POST',
                    data: params,
                    success: function(data){
                        self.channels.push(data);
                    },
                    error: function(error) {
                        console.log(error);
                    }
                });
            }

            this.name = "";
            this.username = "";
            this.password = "";
            this.is_admin = "";
            this.url = "";
        },
        updateClick(){
            self = this;
            params = null;

            if(this.model == 'user'){
                params = JSON.stringify({ 
                    "user_id": this.id, "name": this.name, "username": this.username, 
                    "password": this.password, "is_admin": this.is_admin
                });
                
                $.ajax({
                    url: 'http://127.0.0.1:8000/api/user/update/',
                    contentType: "application/json",
                    dataType: 'json',
                    type: 'POST',
                    data: params,
                    success: function(data){
                        self.users.pop(self.item_to_update);
                        self.users.push(data);
                    },
                    error: function(error) {
                        console.log(error);
                    }
                });
            }

            if(this.model == 'category'){
                params = JSON.stringify({ 
                    "name": this.name, "category_id":this.id
                });

                $.ajax({
                    url: 'http://127.0.0.1:8000/api/category/update/',
                    contentType: "application/json",
                    dataType: 'json',
                    type: 'POST',
                    data: params,
                    success: function(data){
                        self.categories.pop(self.item_to_update);
                        self.categories.push(data);
                    },
                    error: function(error) {
                        console.log(error);
                    }
                });
            }
            
            if(this.model == 'channel'){
                categ_id = this.categ_id.split('-');
                categ_id = categ_id[0]

                params = JSON.stringify({ 
                    "channel_id":this.id, "name": this.name, "url": this.url, "category_id": categ_id
                });

                $.ajax({
                    url: 'http://127.0.0.1:8000/api/channel/update/',
                    contentType: "application/json",
                    dataType: 'json',
                    type: 'POST',
                    data: params,
                    success: function(data){
                        self.channels.pop(self.item_to_update);
                        self.channels.push(data);
                    },
                    error: function(error) {
                        console.log(error);
                    }
                });
            }

            this.id = null;
            this.name = "";
            this.username = "";
            this.password = "";
            this.is_admin = "";
            this.url = "";
            this.operation = "";
            this.item_to_update = null;
        },
        deleteClick(model){
            self = this;
            params = null;

            if(this.model == 'user'){
                params = JSON.stringify({
                    "user_id":this.item_to_delete.id
                });

                $.ajax({
                    url: 'http://127.0.0.1:8000/api/user/delete/',
                    contentType: "application/json",
                    dataType: 'json',
                    type: 'POST',
                    data: params,
                    success: function(data){
                        self.users.pop(self.item_to_delete);
                    },
                    error: function(error) {
                        console.log(error);
                    }
                });

            }

            if(this.model == 'category'){
                params = JSON.stringify({
                    "category_id":this.item_to_delete.id
                });

                $.ajax({
                    url: 'http://127.0.0.1:8000/api/category/delete/',
                    contentType: "application/json",
                    dataType: 'json',
                    type: 'POST',
                    data: params,
                    success: function(data){
                        self.categories.pop(self.item_to_delete);
                    },
                    error: function(error) {
                        console.log(error);
                    }
                });
            }
            
            if(this.model == 'channel'){
                params = JSON.stringify({
                    "channel_id":this.item_to_delete.id
                });

                $.ajax({
                    url: 'http://127.0.0.1:8000/api/channel/delete/',
                    contentType: "application/json",
                    dataType: 'json',
                    type: 'POST',
                    data: params,
                    success: function(data){
                        self.channels.pop(self.item_to_delete);
                    },
                    error: function(error) {
                        console.log(error);
                    }
                });
            }

            this.item_to_delete = {'name':''};
            this.operation = "";
            this.name = "";
        },
        setObjectClick(model, item){
            this.operation = "update";
            this.id = item.id;
            this.model = model;
            this.item_to_update = item;

            if(model == 'user'){
                this.name = item.name;
                this.username = item.username;
                this.password = item.password;
                this.is_admin = item.is_admin;
            }
            else if (model == 'category'){
                this.name = item.name;
            }
            else if (model == 'channel'){
                this.name = item.name;
                this.url = item.url;
                this.categ_id = item.categ_id;
            }
        },
        setObjectToDeleteClick(model, item){
            this.operation = "delete";
            this.model = model;
            this.item_to_delete = item;
        }
    },
    created: function(){
        self = this;

        $.ajax({
            url: 'http://127.0.0.1:8000/api/admin/all/',
            contentType: "application/json",
            dataType: 'json',
            type: 'POST',
            data: {},
            success: function(result){
                //console.log(result);
                self.users = result.data.users;
                self.categories = result.data.categories;
                self.channels = result.data.channels;
            },
            error: function(error) {
                console.log(error);
            }
        });
    }
});