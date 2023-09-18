import React from "react";
import { createRoot } from "react-dom/client";
import "./assets/styles/index.scss";
import HomePage from "./pages/homePage";

export function App() {
  // return <BrowserRouter>
  //     <HomePage/>
  // </BrowserRouter>

  return <HomePage />;
}

// ReactDOM.render(
//   // <Provider store={store}>
//     <ModalProvider>
//       <App />
//     </ModalProvider>,
//   // </Provider>,
//   document.getElementById("root")
//
// )

const container = document.getElementById("root");
const root = createRoot(container); // createRoot(container!) if you use TypeScript
// const store = createStore(reducers)
root.render(
  // <Provider store={store}>
  <App tab="home" />
  // </Provider>
);
