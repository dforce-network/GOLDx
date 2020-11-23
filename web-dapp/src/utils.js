import goldx_abi from './abi/GOLDx.json';
import token_abi from './abi/erc20abi.json';
import address_map from './abi/address_map.json';



export const calc_rate = (that) => {
  var amount_bn = that.bn(10).pow(that.bn(18));

  var base_data_6 = that.state.BaseData[6];
  var base_data_5 = that.state.BaseData[5];
  var base_data_3 = that.state.BaseData[3];
  var base_data_2 = that.state.BaseData[2];
  var base_data_1 = that.state.BaseData[1];
  var base_data_0 = that.state.BaseData[0];
  var amount_to_receive_goldx = amount_bn.sub(amount_bn.mul(that.bn(base_data_6)).div(that.bn(base_data_5)));
  if (that.bn(base_data_2).gt(that.bn(base_data_1))) {
    amount_to_receive_goldx = amount_to_receive_goldx.div(that.bn(10).pow(that.bn(base_data_2).sub(that.bn(base_data_1))));
  } else {
    amount_to_receive_goldx = amount_to_receive_goldx.mul(that.bn(10).pow(that.bn(base_data_1).sub(that.bn(base_data_2))));
  }
  amount_to_receive_goldx = amount_to_receive_goldx.mul(that.bn(base_data_0)).div(that.bn(10).pow(that.bn(18)));
  amount_to_receive_goldx = amount_to_receive_goldx.sub(amount_to_receive_goldx.mul(that.bn(base_data_3)).div(that.bn(10).pow(that.bn(18))));

  that.setState({
    paxg_to_goldx: amount_to_receive_goldx
  })
}
export const calc_rate_plus = (that) => {
  var amount_bn = that.bn(10).pow(that.bn(18));

  var base_data_6 = that.state.BaseData[6];
  var base_data_5 = that.state.BaseData[5];
  var base_data_4 = that.state.BaseData[4];
  var base_data_2 = that.state.BaseData[2];
  var base_data_1 = that.state.BaseData[1];
  var base_data_0 = that.state.BaseData[0];
  var amount_to_receive_paxg = amount_bn.sub(amount_bn.mul(that.bn(base_data_4)).div(that.bn(10).pow(that.bn(18))));
  amount_to_receive_paxg = amount_to_receive_paxg.mul(that.bn(10).pow(that.bn(18))).div(that.bn(base_data_0));
  if (that.bn(base_data_1).gt(that.bn(base_data_2))) {
    amount_to_receive_paxg = amount_to_receive_paxg.div(that.bn(10).pow(that.bn(base_data_1).sub(that.bn(base_data_2))))
  } else {
    amount_to_receive_paxg = amount_to_receive_paxg.mul(that.bn(10).pow(that.bn(base_data_2).sub(that.bn(base_data_1))))
  }
  amount_to_receive_paxg = amount_to_receive_paxg.sub(that.bn(amount_to_receive_paxg).mul(that.bn(base_data_6)).div(that.bn(base_data_5)))

  that.setState({
    goldx_to_paxg: amount_to_receive_paxg
  })
}

export const getBaseData = (contract) => {
  return new Promise((resolve, reject) => {
    contract.methods.getBaseData().call((err, res_BaseData) => {
      // console.log(res_BaseData);
      resolve(res_BaseData);
    });
  })
}

export const get_balanceOf = (contract, nettype) => {
  return new Promise((resolve, reject) => {
    contract.methods.balanceOf(address_map[nettype]['GOLDx']).call((err, res_balanceOf) => {
      resolve(res_balanceOf);
    });
  })
}

export const get_totalSupply = (contract) => {
  return new Promise((resolve, reject) => {
    contract.methods.totalSupply().call((err, res_totalSupply) => {
      // console.log(res_totalSupply);
      resolve(res_totalSupply);
    });
  })
}

export const i_got_hash = (that, action, send_token, send_amount, recive_token, recive_amount, hash, status) => {
  let timestamp = new Date().getTime();
  if (window.localStorage) {
    let key = that.state.my_account + '-' + that.state.net_type;
    let historyData = JSON.parse(window.localStorage.getItem(key)) || [];
    historyData.push({
      action: action,
      account: that.state.my_account,
      net_type: that.state.net_type,
      send_token: send_token,
      send_amount: send_amount,
      recive_token: recive_token,
      recive_amount: recive_amount,
      hash: hash,
      timestamp: timestamp,
      status: status
    });
    window.localStorage.setItem(key, JSON.stringify(historyData));
    console.log('got hash && setItem.');

    that.setState({ load_new_history: Math.random() });
  }
}


// input change
export const paxg_change = (that, value) => {
  try {
    var reg = new RegExp("[\\u4E00-\\u9FFF]+", "g");
    var rega_Z = /[a-z]/g;

    // alert(rega_Z.test(value));
    if (reg.test(value)) {
      that.setState({ value_paxg: '', });
      return console.log('reg.test(value)');
    }
    if (rega_Z.test(value)) {
      that.setState({ value_paxg: '', });
      return console.log('reg.test(value)');
    }


    if (!that.state.is_already) {
      return console.log('not already...');
    }
    if (value.indexOf('.') > 0) {
      var part2 = value.split('.')[1];
      // console.log(part2);
      if (part2.length > 6) {
        return console.log('>6');
      }
    }

    that.setState({
      i_mint_max: false,
    })

    var amount_bn;
    var temp_value = value;
    if (temp_value.indexOf('.') > 0) { // 123.456
      var sub_num = temp_value.length - temp_value.indexOf('.') - 1; // 3
      temp_value = temp_value.substr(0, temp_value.indexOf('.')) + temp_value.substr(value.indexOf('.') + 1); // '123456'
      amount_bn = that.bn(temp_value).mul(that.bn(10 ** (18 - sub_num))); // bn_'123456 10**15'
    } else {
      amount_bn = that.bn(value).mul(that.bn(10 ** 18));
    }


    var base_data_6 = that.state.BaseData[6];
    var base_data_5 = that.state.BaseData[5];
    var base_data_3 = that.state.BaseData[3];
    var base_data_2 = that.state.BaseData[2];
    var base_data_1 = that.state.BaseData[1];
    var base_data_0 = that.state.BaseData[0];
    var amount_to_receive_goldx = amount_bn.sub(amount_bn.mul(that.bn(base_data_6)).div(that.bn(base_data_5)));
    if (that.bn(base_data_2).gt(that.bn(base_data_1))) {
      amount_to_receive_goldx = amount_to_receive_goldx.div(that.bn(10).pow(that.bn(base_data_2).sub(that.bn(base_data_1))));
    } else {
      amount_to_receive_goldx = amount_to_receive_goldx.mul(that.bn(10).pow(that.bn(base_data_1).sub(that.bn(base_data_2))));
    }
    amount_to_receive_goldx = amount_to_receive_goldx.mul(that.bn(base_data_0)).div(that.bn(10).pow(that.bn(18)));
    amount_to_receive_goldx = amount_to_receive_goldx.sub(amount_to_receive_goldx.mul(that.bn(base_data_3)).div(that.bn(10).pow(that.bn(18))));


    that.setState({
      value_paxg: value,
      value_paxg_bn: amount_bn,
      to_receive_goldx: format_bn(amount_to_receive_goldx, 18, 6),
      to_receive_goldx_bn: amount_to_receive_goldx,
      is_btn_disabled_mint: false
    }, () => {
      console.log('send: ', that.state.value_paxg_bn.toLocaleString(), 'receive: ', that.state.to_receive_goldx_bn.toLocaleString())
      if (amount_bn.gt(that.bn(that.state.my_balance_paxg))) {
        console.log('extends...');
        paxg_click_max(that);
      }
    })
  } catch (error) {
    console.log(error)
  }
}
export const paxg_click_max = (that) => {
  // console.log(that.state.my_balance_paxg);
  if (!that.state.my_balance_paxg) {
    return console.log('not get my_balance_paxg yet');
  }

  if (that.bn(that.state.my_balance_paxg).lte(that.bn(0))) {
    console.log('balance is 0');
    that.setState({
      is_btn_disabled_mint: true
    })
  }

  that.setState({
    i_mint_max: true,
  })

  var amount_bn = that.bn(that.state.my_balance_paxg);
  var base_data_6 = that.state.BaseData[6];
  var base_data_5 = that.state.BaseData[5];
  var base_data_3 = that.state.BaseData[3];
  var base_data_2 = that.state.BaseData[2];
  var base_data_1 = that.state.BaseData[1];
  var base_data_0 = that.state.BaseData[0];
  var amount_to_receive_goldx = amount_bn.sub(amount_bn.mul(that.bn(base_data_6)).div(that.bn(base_data_5)));
  if (that.bn(base_data_2).gt(that.bn(base_data_1))) {
    amount_to_receive_goldx = amount_to_receive_goldx.div(that.bn(10).pow(that.bn(base_data_2).sub(that.bn(base_data_1))));
  } else {
    amount_to_receive_goldx = amount_to_receive_goldx.mul(that.bn(10).pow(that.bn(base_data_1).sub(that.bn(base_data_2))));
  }
  amount_to_receive_goldx = amount_to_receive_goldx.mul(that.bn(base_data_0)).div(that.bn(10).pow(that.bn(18)));
  amount_to_receive_goldx = amount_to_receive_goldx.sub(amount_to_receive_goldx.mul(that.bn(base_data_3)).div(that.bn(10).pow(that.bn(18))));

  that.setState({
    value_paxg: format_bn(that.state.my_balance_paxg, 18, 6),
    value_paxg_bn: that.state.my_balance_paxg,
    to_receive_goldx: format_bn(amount_to_receive_goldx, 18, 6),
    to_receive_goldx_bn: amount_to_receive_goldx
  })
}
export const goldx_change = (that, value) => {
  try {
    var reg = new RegExp("[\\u4E00-\\u9FFF]+", "g");
    var rega_Z = /[a-z]/g;

    // alert(rega_Z.test(value));
    if (reg.test(value)) {
      that.setState({ value_goldx: '', });
      return console.log('reg.test(value)');
    }
    if (rega_Z.test(value)) {
      that.setState({ value_goldx: '', });
      return console.log('reg.test(value)');
    }


    if (!that.state.is_already) {
      return console.log('not already...');
    }
    if (value.indexOf('.') > 0) {
      var part2 = value.split('.')[1];
      if (part2.length > 6) {
        return console.log('>6');
      }
    }

    that.setState({
      i_redeem_max: false,
    })

    var amount_bn;
    var temp_value = value;
    if (temp_value.indexOf('.') > 0) { // 123.456
      var sub_num = temp_value.length - temp_value.indexOf('.') - 1; // 3
      temp_value = temp_value.substr(0, temp_value.indexOf('.')) + temp_value.substr(value.indexOf('.') + 1); // '123456'
      amount_bn = that.bn(temp_value).mul(that.bn(10 ** (18 - sub_num))); // bn_'123456 10**15'
    } else {
      amount_bn = that.bn(value).mul(that.bn(10 ** 18));
    }


    var base_data_6 = that.state.BaseData[6];
    var base_data_5 = that.state.BaseData[5];
    var base_data_4 = that.state.BaseData[4];
    var base_data_2 = that.state.BaseData[2];
    var base_data_1 = that.state.BaseData[1];
    var base_data_0 = that.state.BaseData[0];
    var amount_to_receive_paxg = amount_bn.sub(amount_bn.mul(that.bn(base_data_4)).div(that.bn(10).pow(that.bn(18))));
    amount_to_receive_paxg = amount_to_receive_paxg.mul(that.bn(10).pow(that.bn(18))).div(that.bn(base_data_0));
    if (that.bn(base_data_1).gt(that.bn(base_data_2))) {
      amount_to_receive_paxg = amount_to_receive_paxg.div(that.bn(10).pow(that.bn(base_data_1).sub(that.bn(base_data_2))))
    } else {
      amount_to_receive_paxg = amount_to_receive_paxg.mul(that.bn(10).pow(that.bn(base_data_2).sub(that.bn(base_data_1))))
    }
    amount_to_receive_paxg = amount_to_receive_paxg.sub(that.bn(amount_to_receive_paxg).mul(that.bn(base_data_6)).div(that.bn(base_data_5)))


    that.setState({
      value_goldx: value,
      value_goldx_bn: amount_bn,
      to_receive_paxg: format_bn(amount_to_receive_paxg, 18, 6),
      to_receive_paxg_bn: amount_to_receive_paxg,
      is_btn_disabled_redeem: false
    }, () => {
      console.log('send: ', that.state.value_goldx_bn.toLocaleString(), 'receive: ', that.state.to_receive_paxg_bn.toLocaleString())
      if (amount_bn.gt(that.bn(that.state.my_balance_goldx))) {
        console.log('extends...');
        goldx_click_max(that);
      }
    })
  } catch (error) {
    console.log(error)
  }
}
export const goldx_click_max = (that) => {
  // console.log(that.state.my_balance_goldx);
  if (!that.state.my_balance_goldx) {
    return console.log('not get my_balance_goldx yet');
  }

  if (that.bn(that.state.my_balance_goldx).lte(that.bn(0))) {
    console.log('balance is 0');
    that.setState({
      is_btn_disabled_redeem: true
    })
  }

  that.setState({
    i_redeem_max: true
  })

  var amount_bn = that.bn(that.state.my_balance_goldx);
  var base_data_6 = that.state.BaseData[6];
  var base_data_5 = that.state.BaseData[5];
  var base_data_4 = that.state.BaseData[4];
  var base_data_2 = that.state.BaseData[2];
  var base_data_1 = that.state.BaseData[1];
  var base_data_0 = that.state.BaseData[0];
  var amount_to_receive_paxg = amount_bn.sub(amount_bn.mul(that.bn(base_data_4)).div(that.bn(10).pow(that.bn(18))));
  amount_to_receive_paxg = amount_to_receive_paxg.mul(that.bn(10).pow(that.bn(18))).div(that.bn(base_data_0));
  if (that.bn(base_data_1).gt(that.bn(base_data_2))) {
    amount_to_receive_paxg = amount_to_receive_paxg.div(that.bn(10).pow(that.bn(base_data_1).sub(that.bn(base_data_2))))
  } else {
    amount_to_receive_paxg = amount_to_receive_paxg.mul(that.bn(10).pow(that.bn(base_data_2).sub(that.bn(base_data_1))))
  }
  amount_to_receive_paxg = amount_to_receive_paxg.sub(that.bn(amount_to_receive_paxg).mul(that.bn(base_data_6)).div(that.bn(base_data_5)))

  that.setState({
    value_goldx: format_bn(that.state.my_balance_goldx, 18, 6),
    value_goldx_bn: that.state.my_balance_goldx,
    to_receive_paxg: format_bn(amount_to_receive_paxg, 18, 6),
    to_receive_paxg_bn: amount_to_receive_paxg
  })
}

// btn click
export const click_mint = (that) => {
  if (!that.state.value_paxg_bn) {
    return console.log('pls input number.');
  }
  if (Number(that.state.value_paxg) === 0) {
    return console.log('u input number 0.');
  }

  that.setState({
    is_btn_disabled_mint: true
  })

  var max_num = that.bn(2).pow(that.bn(256)).sub(that.bn(1));
  // console.log('send: ', that.state.value_paxg_bn.toLocaleString(), 'receive: ', that.state.to_receive_goldx_bn.toLocaleString())

  if (!that.state.is_approve) {
    console.log('is_approve: ', that.state.is_approve);
    that.state.contract_PAXG.methods.approve(address_map[that.state.net_type]['GOLDx'], max_num).send(
      {
        from: that.state.my_account,
      }, (reject, res_hash) => {
        if (res_hash) {
          that.state.contract_GOLDx.methods.mint(that.state.my_account, that.state.value_paxg_bn).send(
            {
              from: that.state.my_account,
              gas: 250000
            }, (reject, res_hash) => {
              if (res_hash) {
                console.log(res_hash);
                i_got_hash(that, 'mint', 'PAXG', that.state.value_paxg_bn.toLocaleString(), 'Goldx', that.state.to_receive_goldx_bn.toLocaleString(), res_hash, 'pendding');
                that.setState({
                  value_paxg: '',
                  value_paxg_bn: '',
                  to_receive_goldx: '',
                  to_receive_goldx_bn: '',
                  is_btn_disabled_mint: false
                })
              }
              if (reject) {
                that.setState({
                  is_btn_disabled_mint: false
                })
              }
            }
          )
        }
        if (reject) {
          that.setState({
            is_btn_disabled_mint: false
          })
        }
      }
    )
  } else {
    console.log('is_approve: ', that.state.is_approve);
    that.state.contract_GOLDx.methods.mint(that.state.my_account, that.state.value_paxg_bn).send(
      {
        from: that.state.my_account,
        gas: 250000
      }, (reject, res_hash) => {
        if (res_hash) {
          console.log(res_hash);
          i_got_hash(that, 'mint', 'PAXG', that.state.value_paxg_bn.toLocaleString(), 'Goldx', that.state.to_receive_goldx_bn.toLocaleString(), res_hash, 'pendding');
          that.setState({
            value_paxg: '',
            value_paxg_bn: '',
            to_receive_goldx: '',
            to_receive_goldx_bn: '',
            is_btn_disabled_mint: false
          })
        }
        if (reject) {
          that.setState({
            is_btn_disabled_mint: false
          })
        }
      }
    )
  }
}
export const click_redeem = (that) => {
  if (!that.state.value_goldx_bn) {
    return console.log('pls input number.');
  }
  if (Number(that.state.value_goldx) === 0) {
    return console.log('u input number 0.');
  }

  that.setState({
    is_btn_disabled_redeem: true
  })


  that.state.contract_GOLDx.methods.burn(that.state.my_account, that.state.value_goldx_bn).send(
    {
      from: that.state.my_account,
      gas: 250000
    }, (reject, res_hash) => {
      if (res_hash) {
        console.log(res_hash);
        i_got_hash(that, 'redeem', 'Goldx', that.state.value_goldx_bn.toLocaleString(), 'PAXG', that.state.to_receive_paxg_bn.toLocaleString(), res_hash, 'pendding');
        that.setState({
          value_goldx: '',
          value_goldx_bn: '',
          to_receive_paxg: '',
          to_receive_paxg_bn: '',
          is_btn_disabled_redeem: false
        })
      }
      if (reject) {
        that.setState({
          is_btn_disabled_redeem: false
        })
      }
    }
  )
}


export const format_num_to_K = (str_num) => {
  var part_a = str_num.split('.')[0];
  var part_b = str_num.split('.')[1];

  var reg = /\d{1,3}(?=(\d{3})+$)/g;
  part_a = (part_a + '').replace(reg, '$&,');

  return part_a + '.' + part_b;
}

export const get_nettype = (instance_web3) => {
  return new Promise((resolve, reject) => {
    instance_web3.eth.net.getNetworkType().then(net_type => {
      // console.log(net_type);
      resolve(net_type);
    })
  })
}

export const init_contract = (instance_web3, nettype, token) => {
  // console.log(instance_web3, nettype, token)
  // if (!address_map[nettype]) {
  //   console.log('err net')
  //   return false;
  // }

  return new Promise((resolve, reject) => {
    let contract = new instance_web3.eth.Contract(token === 'GOLDx' ? goldx_abi : token_abi, address_map[nettype][token]);
    if (!address_map[nettype]) {
      reject('err')
    }
    // console.log(contract);
    if (!contract) { reject('err') }
    resolve(contract);
  })
}

export const get_my_account = (instance_web3) => {
  return new Promise((resolve, reject) => {
    instance_web3.givenProvider.enable().then((res_accounts) => {
      if (!res_accounts) { reject('err') };
      // console.log(res_accounts[0]);
      resolve(res_accounts[0]);
    })
  })
}

export const check_approve = (contract_PAXG, my_account, nettype) => {
  return new Promise((resolve, reject) => {
    contract_PAXG.methods.allowance(my_account, address_map[nettype]['GOLDx']).call((err, res_allowance) => {
      resolve(res_allowance);
    });
  })
}

export const get_my_balance = (contract, account) => {
  return new Promise((resolve, reject) => {
    contract.methods.balanceOf(account).call((err, res_balance) => {
      // console.log(err, res_balance);
      if (res_balance) {
        resolve(res_balance)
      } else {
        reject('get balance err')
      }
    });
  })
}

export const get_my_eth = (new_web3, account) => {
  return new Promise((resolve, reject) => {
    new_web3.eth.getBalance(account, (err, res_eth) => {
      resolve(res_eth)
    })
  })
}


export const format_bn = (numStr, decimals, decimalPlace = decimals) => {
  numStr = numStr.toLocaleString().replace(/,/g, '');
  // decimals = decimals.toString();

  // var str = (10 ** decimals).toLocaleString().replace(/,/g, '').slice(1);
  var str = Number(`1e+${decimals}`).toLocaleString().replace(/,/g, '').slice(1);

  var res = (numStr.length > decimals ?
    numStr.slice(0, numStr.length - decimals) + '.' + numStr.slice(numStr.length - decimals) :
    '0.' + str.slice(0, str.length - numStr.length) + numStr).replace(/(0+)$/g, "");

  res = res.slice(-1) === '.' ? res + '00' : res;

  if (decimalPlace === 0)
    return res.slice(0, res.indexOf('.'));

  var length = res.indexOf('.') + 1 + decimalPlace;
  return res.slice(0, length >= res.length ? res.length : length);
  // return res.slice(-1) == '.' ? res + '00' : res;
}


