export default class APISerive {
   //  static UpdateArticle(article_id,body,token){
   //      return fetch(`http://127.0.0.1:8000/api/articles/${article_id}/`,{
   //          method:'PUT',
   //          headers: {
   //              'Content-Type': 'application/json',
   //              'Authorization': `Token ${token}`
   //          },
   //          body:JSON.stringify(body)
   //      }).then(resp => resp.json())
   //  }

   //  static InsertArticle(body,token){
   //      return fetch(`http://127.0.0.1:8000/api/articles/`,{
   //          method:'POST',
   //          headers: {
   //              'Content-Type': 'application/json',
   //              'Authorization': `Token ${token}`
   //          },
   //          body:JSON.stringify(body)
   //      }).then(resp => resp.json())
   //  }

   //  static DeleteArticle(article_id,token){
   //      return fetch(`http://127.0.0.1:8000/api/articles/${article_id}/`,{
   //          method:'PUT',
   //          headers: {
   //              'Content-Type': 'application/json',
   //              'Authorization': `Token ${token}`
   //          }
   //      })
   //  }


    static LoginUser(body){
        return fetch(`http://127.0.0.1:9000/login/`,{
            method:'POST',
            headers: {
                'Content-Type': 'application/json',
                'Cookie': 'csrftoken=n7WsAD8HCiJgcQKKfppgv6Y6mu0EArRI; sessionid=0xz46zg8ij628ylpz0l0ydynk8jgtnvv'
            },
            body:JSON.stringify(body)
        }).then(resp => resp.json())
    }

    static async GetAllProducts(body){
        let resp = await fetch(`http://127.0.0.1:9000/get-all-products`,{
            method:'GET',
            headers: {
                'Content-Type': 'application/json',
                'Cookie': 'csrftoken=n7WsAD8HCiJgcQKKfppgv6Y6mu0EArRI; sessionid=0xz46zg8ij628ylpz0l0ydynk8jgtnvv'
            },
            body:JSON.stringify(body)
        })
        resp = await resp.json()
        return resp.data
    }



    static RegisterUser(body){
        return fetch(`http://127.0.0.1:8000/api/users/`, {
            method:'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body:JSON.stringify(body)
        }).then(resp => resp.json())
    }    

    

}