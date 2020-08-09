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
    },
    methods:{
        setModelClick(model, operation){
            this.model = model;
            this.operation = operation;
        },
        createClick(){
            self = this;

            if(self.model == 'user'){
                self.request_data = JSON.stringify({ 
                    "model": "user", "name": self.name, "username": self.username, 
                    "password": self.password, "is_admin": self.is_admin
                });
            }

            if(self.model == 'category'){
                self.request_data = JSON.stringify({ 
                    "model": "category", "name": self.name
                });
            }
            
            if(self.model == 'channel'){
                categ_id = self.categ_id.split('-');
                categ_id = categ_id[0]

                self.request_data = JSON.stringify({ 
                    "model": "channel", "name": self.name, "url": self.url, "category_id": categ_id
                });
            }
            $.ajax({
                url: 'http://127.0.0.1:8000/api/crud/create/',
                contentType: "application/json",
                dataType: 'json',
                type: 'POST',
                data: self.request_data,
                success: function(result){
                    if(self.model == 'user'){
                        self.users.push(result);
                    }
                    if(self.model == 'category'){
                        self.categories.push(result);
                    }
                    if(self.model == 'channel'){
                        self.channels.push(result);
                    }
                },
                error: function(error) {
                    console.log(error);
                }
            });

            self.name = "";
            self.username = "";
            self.password = "";
            self.is_admin = "";
            self.url = "";
        },
        updateClick(){
            self = this;

            if(self.model == 'user'){
                self.request_data = JSON.stringify({ 
                    "model": "user", "res_id":self.id, "name": self.name, "username": self.username, 
                    "password": self.password, "is_admin": self.is_admin
                });
            }

            if(self.model == 'category'){
                self.request_data = JSON.stringify({ 
                    "model": "category", "name": self.name, "res_id":self.id
                });
            }
            
            if(self.model == 'channel'){
                categ_id = self.categ_id.split('-');
                categ_id = categ_id[0]

                self.request_data = JSON.stringify({ 
                    "model": "channel", "res_id":self.id, "name": self.name, "url": self.url, "category_id": categ_id
                });
            }
            console.log(self.request_data);
            console.log(self.model);
            $.ajax({
                url: 'http://127.0.0.1:8000/api/crud/update/',
                contentType: "application/json",
                dataType: 'json',
                type: 'POST',
                data: self.request_data,
                success: function(result){
                    if(self.model == 'user'){
                        self.users.pop(self.item_to_update);
                        self.users.push(result);
                    }
                    if(self.model == 'category'){
                        self.categories.pop(self.item_to_update);
                        self.categories.push(result);
                    }
                    if(self.model == 'channel'){
                        self.channels.pop(self.item_to_update);
                        self.channels.push(result);
                    }
                },
                error: function(error) {
                   console.log(error);
                }
            });

            self.id = null;
            self.name = "";
            self.username = "";
            self.password = "";
            self.is_admin = "";
            self.url = "";
            self.operation = "";
            self.item_to_update = null;
        },
        deleteClick(model){
            self = this;

            if(self.model == 'user'){
                self.request_data = JSON.stringify({
                    "model": "user", "res_id":self.item_to_delete.id
                });
            }

            if(self.model == 'category'){
                self.request_data = JSON.stringify({
                    "model": "category", "res_id":self.item_to_delete.id
                });
            }
            
            if(self.model == 'channel'){
                self.request_data = JSON.stringify({
                    "model": "channel", "res_id":self.item_to_delete.id
                });
            }

            $.ajax({
                url: 'http://127.0.0.1:8000/api/crud/delete/',
                contentType: "application/json",
                dataType: 'json',
                type: 'POST',
                data: self.request_data,
                success: function(result){
                    if(self.model == 'user'){
                        self.users.pop(self.item_to_delete);
                    }
                    if(self.model == 'category'){
                        self.categories.pop(self.item_to_delete);
                    }
                    if(self.model == 'channel'){
                        self.channels.pop(self.item_to_delete);
                    }
                },
                error: function(error) {
                   console.log(error);
                }
            });

            self.item_to_delete = {'name':''};
            self.operation = "";
            self.name = "";
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
        that = this;
        $.ajax({
            url: 'http://127.0.0.1:8000/api/crud/all/',
            contentType: "application/json",
            dataType: 'json',
            type: 'GET',
            success: function(result){
                //console.log(result.data.users);
                that.users = result.data.users;
                that.categories = result.data.categories;
                that.channels = result.data.channels;
            },
            error: function(error) {
                console.log(error);
            }
        });
    }
});