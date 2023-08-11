var mix = {
	methods: {
		submitPayment() {
			console.log('qweqwewqeqweqw')
			const orderId = location.pathname.startsWith('/payment/')
				? Number(location.pathname.replace('/payment/', '').replace('/', ''))
				: null

			const paymentData = {
    			name: this.name,
    			number: this.number,
    			year: this.year,
    			month: this.month,
    			code: this.code
  			};
			this.showSpinner = true;

			const minDelay = 5000;
			const maxDelay = 15000;
			const randomDelay = Math.floor(Math.random() * (maxDelay - minDelay + 1) + minDelay);

			setTimeout(() => {
			this.postData(`/api/payment/${orderId}/`, paymentData)
				.then((response) => {
					if (response.data.error_message) {
						alert(response.data.error_message);
						location.assign('/');
					} else {
						alert('Успешная оплата')
						this.number = ''
						this.name = ''
						this.year = ''
						this.month = ''
						this.code = ''
						location.assign('/')
					}
				})
				.catch((error) => {
					console.warn('Ошибка при оплате', error)
				});
			}, randomDelay);
			return false;
		},
	},
	data() {
		return {
			number: '',
			month: '',
			year: '',
			name: '',
			code: '',
			showSpinner: false,
		}
	}
}