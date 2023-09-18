// export default (state = initialState, action) => {
//     switch (action.type) {
//         case types.popUpClose:
//         case types.popUpOpen:
//         case types.popUpCloseDouble:
//         case types.popUpOpenDouble: {
//             return {
//                 ...state,
//                 popUpState: action.type,
//             };
//         }
//         default: {
//             return state;
//         }
//     }
// };

// const initialState = {
//     items: [1, 2, 3, 4],
//     busy: false
// };
//
// const items = function(items = data.items, { type, payload }) {
//     if (type === "more") {
//         return items.concat([payload]);
//     }
//
//     return items;
// };
//
// const reducer = (state, action) => {
//     console.log('reducer called');
//     return state;
// };
//
// export default reducer()
