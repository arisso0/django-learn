var mix = {
	methods: {
		submitPayment() {
			console.log('payment-someone')
			const orderId = location.pathname.startsWith('/payment-someone/')
				? Number(location.pathname.replace('/payment-someone/', '').replace('/', ''))
				: null

			const paymentData = {
    			number: this.number,
  			};

			this.showSpinner = true;

			const minDelay = 5000;
			const maxDelay = 15000;
			const randomDelay = Math.floor(Math.random() * (maxDelay - minDelay + 1) + minDelay);


			setTimeout(() => {
				this.postData(`/api/payment-someone/${orderId}/`, paymentData)
					.then((response) => {
						if (response.data.error_message) {
						alert(response.data.error_message);
						location.assign('/');
						} else {
							alert('Успешная оплата');
							this.number = '';
							location.assign('/');
						}
					})
					.catch((error) => {
						console.warn('Ошибка при оплате', error);
						location.assign('/');
					});
				}, randomDelay);
			return false;
			},
		generateRandomNumber() {
			let billNumber = '';
			do {
				billNumber = Math.random() + '';
				billNumber = billNumber.slice(-17, -1);
			} while (parseFloat(billNumber) % 2 !== 0);
			this.number = billNumber;
			},
    },
	data() {
		return {
			number: '',
			showSpinner: false,
		}
	}
}