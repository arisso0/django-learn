var mix = {
	methods: {
		signUp () {
			const username = document.querySelector('#login').value
			const password = document.querySelector('#password').value
			const name = document.querySelector('#first_name').value

			const formData = new FormData()
			formData.append('username', username)
  			formData.append('password', password)
  			formData.append('first_name', name)

			this.postData('/api/sign-up/', formData)
				.then(({ data, status }) => {
					location.assign(`/`)
				})
		}
	},
	mounted() {
	},
	data() {
		return {}
	}
}