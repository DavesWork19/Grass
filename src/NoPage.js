import { useNavigate } from "react-router-dom";

const NoPage = () => {
    const navigate = useNavigate();
    const handleButtonClick = navigation => {
        navigate(navigation);
    }

    return (
        <>
            <header className="container mb-4 mt-2">
                <h1 className="text-center">The Numbers Game</h1>
            </header>
            <main className="container">
                <div>
                    This page does not exist - please visit a valid page.
                </div>
                <button type="button" onClick={() => handleButtonClick("/")} className="btn btn-light border">
                    Home
                </button>
            </main>
        </>
    );
}

export default NoPage;
