import { useEffect, useState } from "react";

const API_BASE = "/api";

function App() {
  const [collections, setCollections] = useState([]);
  const [newCollectionName, setNewCollectionName] = useState("");
  const [newSetNames, setNewSetNames] = useState({});
  const [newCardInputs, setNewCardInputs] = useState({});
  const [error, setError] = useState(null);

  useEffect(() => {
    loadCollections();
  }, []);

  async function loadCollections() {
    setError(null);
    try {
      const res = await fetch(`${API_BASE}/collections`);
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || "Failed to load collections");
      setCollections(data);
    } catch (err) {
      setError(err.message);
    }
  }

  async function handleCreateCollection(event) {
    event.preventDefault();
    if (!newCollectionName.trim()) return;

    const res = await fetch(`${API_BASE}/collections`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name: newCollectionName.trim() }),
    });

    if (!res.ok) {
      const payload = await res.json();
      setError(payload.error || "Unable to create collection");
      return;
    }

    setNewCollectionName("");
    loadCollections();
  }

  async function handleCreateSet(collectionId) {
    const setName = newSetNames[collectionId]?.trim();
    if (!setName) return;

    const res = await fetch(`${API_BASE}/sets`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name: setName, collectionId }),
    });

    if (!res.ok) {
      const payload = await res.json();
      setError(payload.error || "Unable to create set");
      return;
    }

    setNewSetNames((prev) => ({ ...prev, [collectionId]: "" }));
    loadCollections();
  }

  async function handleCreateCard(setId) {
    const card = newCardInputs[setId] || {};
    if (!card.name?.trim() || !card.number) return;

    const res = await fetch(`${API_BASE}/cards`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        name: card.name.trim(),
        setId,
        number: Number(card.number),
      }),
    });

    if (!res.ok) {
      const payload = await res.json();
      setError(payload.error || "Unable to create card");
      return;
    }

    setNewCardInputs((prev) => ({ ...prev, [setId]: { name: "", number: "" } }));
    loadCollections();
  }

  async function handleDeleteCollection(collectionId) {
    const res = await fetch(`${API_BASE}/collections/${collectionId}`, {
      method: "DELETE",
    });
    if (!res.ok) {
      const payload = await res.json();
      setError(payload.error || "Unable to delete collection");
      return;
    }
    loadCollections();
  }

  async function handleDeleteSet(setId) {
    const res = await fetch(`${API_BASE}/sets/${setId}`, {
      method: "DELETE",
    });
    if (!res.ok) {
      const payload = await res.json();
      setError(payload.error || "Unable to delete set");
      return;
    }
    loadCollections();
  }

  async function handleDeleteCard(cardId) {
    const res = await fetch(`${API_BASE}/cards/${cardId}`, {
      method: "DELETE",
    });
    if (!res.ok) {
      const payload = await res.json();
      setError(payload.error || "Unable to delete card");
      return;
    }
    loadCollections();
  }

  return (
    <div className="app-container">
      <header>
        <h1>Card Collector</h1>
      </header>

      <section className="panel">
        <h2>Create new collection</h2>
        <form onSubmit={handleCreateCollection} className="row-form">
          <input
            value={newCollectionName}
            onChange={(event) => setNewCollectionName(event.target.value)}
            placeholder="Collection name"
          />
          <button type="submit">Create</button>
        </form>
      </section>

      {error && <div className="error">{error}</div>}

      <section className="panel">
        <h2>Collections</h2>
        {collections.length === 0 ? (
          <p>No collections found.</p>
        ) : (
          collections.map((collection) => (
            <div key={collection.id} className="card">
              <div className="collection-header">
                <h3>{collection.name}</h3>
                <div>
                  <span>ID: {collection.id}</span>
                  <button
                    className="delete-button"
                    onClick={() => handleDeleteCollection(collection.id)}
                  >
                    Delete
                  </button>
                </div>
              </div>

              <div className="card-body">
                <form
                  className="row-form"
                  onSubmit={(event) => {
                    event.preventDefault();
                    handleCreateSet(collection.id);
                  }}
                >
                  <input
                    value={newSetNames[collection.id] || ""}
                    onChange={(event) =>
                      setNewSetNames((prev) => ({
                        ...prev,
                        [collection.id]: event.target.value,
                      }))
                    }
                    placeholder="New set name"
                  />
                  <button type="submit">Add set</button>
                </form>

                {collection.sets.length === 0 ? (
                  <p className="small-text">No sets in this collection yet.</p>
                ) : (
                  collection.sets.map((setItem) => (
                    <div key={setItem.id} className="set-card">
                      <div className="collection-header">
                        <h4>{setItem.name}</h4>
                        <div>
                          <span>Set ID: {setItem.id}</span>
                          <button
                            className="delete-button"
                            onClick={() => handleDeleteSet(setItem.id)}
                          >
                            Delete
                          </button>
                        </div>
                      </div>

                      <form
                        className="row-form"
                        onSubmit={(event) => {
                          event.preventDefault();
                          handleCreateCard(setItem.id);
                        }}
                      >
                        <input
                          value={newCardInputs[setItem.id]?.name || ""}
                          onChange={(event) =>
                            setNewCardInputs((prev) => ({
                              ...prev,
                              [setItem.id]: {
                                ...(prev[setItem.id] || {}),
                                name: event.target.value,
                              },
                            }))
                          }
                          placeholder="Card name"
                        />
                        <input
                          type="number"
                          value={newCardInputs[setItem.id]?.number || ""}
                          onChange={(event) =>
                            setNewCardInputs((prev) => ({
                              ...prev,
                              [setItem.id]: {
                                ...(prev[setItem.id] || {}),
                                number: event.target.value,
                              },
                            }))
                          }
                          placeholder="Card number"
                        />
                        <button type="submit">Add card</button>
                      </form>

                      {setItem.cards.length === 0 ? (
                        <p className="small-text">No cards yet.</p>
                      ) : (
                        <ul className="nested-list">
                          {setItem.cards.map((card) => (
                            <li key={card.id} className="card-item">
                              <span>
                                {card.name} (#{card.number})
                              </span>
                              <button
                                className="delete-button small"
                                onClick={() => handleDeleteCard(card.id)}
                              >
                                Delete
                              </button>
                            </li>
                          ))}
                        </ul>
                      )}
                    </div>
                  ))
                )}
              </div>
            </div>
          ))
        )}
      </section>
    </div>
  );
}

export default App;
