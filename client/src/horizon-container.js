import Horizon from '@horizon/client'

const _horizon = Horizon();

export default {
  get: () => _horizon,
  // clearAuthTokens: () => Horizon.clearAuthTokens(),
  // getCurrentUser: (callback) => {
  //     _horizon.currentUser().fetch().subscribe(user => callback(user));
  // }
}