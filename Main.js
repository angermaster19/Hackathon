import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Loader2 } from "lucide-react";

export default function Home() {
  const [isLoading, setIsLoading] = useState(false);
  const [showAuth, setShowAuth] = useState(true);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [userId, setUserId] = useState(null);
  const [formData, setFormData] = useState({
    houseSize: "",
    bedrooms: "",
    location: "",
    furnished: "fully",
  });
  const [prediction, setPrediction] = useState("");

  const appSlug = "home-price-predictor";

  useEffect(() => {
    const storedUserId = localStorage.getItem("userId");
    if (storedUserId) {
      setUserId(storedUserId);
      setShowAuth(false);
    }
  }, []);

  const handleAuth = async (type) => {
    if (!email || !password) {
      alert("Please fill in all fields");
      return;
    }

    setIsLoading(true);

    try {
      const response = await fetch("https://r0c8kgwocscg8gsokogwwsw4.zetaverse.one/db", {
        method: "POST",
        headers: {
          Authorization: "Bearer ZgwQPsvoZqdTFfu5xF19Nw3wTOY2",
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          action: type === "login" ? "read" : "create",
          table: "users",
          appSlug,
          userId: email,
          data: { password },
        }),
      });

      const data = await response.json();

      if (type === "login" && data.data.length === 0) {
        alert("User not found or incorrect password");
        return;
      }

      setUserId(email);
      localStorage.setItem("userId", email);
      setShowAuth(false);
    } catch (error) {
      alert("Authentication failed");
      console.error(error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem("userId");
    setUserId(null);
    setShowAuth(true);
  };

  const predictPrice = async () => {
    const { houseSize, bedrooms, location, furnished } = formData;

    if (!houseSize || !bedrooms || !location) {
      alert("Please fill in all fields");
      return;
    }

    setIsLoading(true);

    try {
      const response = await fetch("https://r0c8kgwocscg8gsokogwwsw4.zetaverse.one/ai", {
        method: "POST",
        headers: {
          Authorization: "Bearer ZgwQPsvoZqdTFfu5xF19Nw3wTOY2",
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          messages: [{
            role: "user",
            content: [{
              type: "text",
              text: `Predict the house price for a ${houseSize} sq ft house with ${bedrooms} bedrooms in ${location}, ${furnished} furnished. Give the answer in USD with a range.`,
            }],
          }],
        }),
      });

      const data = await response.json();
      setPrediction(data.message);

      await savePrediction({
        ...formData,
        prediction: data.message,
      });
    } catch (error) {
      alert("Prediction failed");
      console.error(error);
    } finally {
      setIsLoading(false);
    }
  };

  const savePrediction = async (predictionData) => {
    try {
      await fetch("https://r0c8kgwocscg8gsokogwwsw4.zetaverse.one/db", {
        method: "POST",
        headers: {
          Authorization: "Bearer ZgwQPsvoZqdTFfu5xF19Nw3wTOY2",
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          action: "create",
          table: "predictions",
          appSlug,
          userId,
          data: predictionData,
        }),
      });
    } catch (error) {
      console.error("Failed to save prediction:", error);
    }
  };

  return (
    <div className="bg-gray-50 min-h-screen">
      {isLoading && (
        <div className="fixed inset-0 bg-white/90 flex items-center justify-center z-50">
          <Loader2 className="h-12 w-12 animate-spin text-blue-500" />
        </div>
      )}

      {showAuth ? (
        <div className="min-h-screen flex items-center justify-center px-4">
          <div className="bg-white p-8 rounded-lg shadow-lg max-w-md w-full">
            <div className="text-center mb-8">
              <h2 className="text-2xl font-bold text-gray-800">Welcome to HomePrice Predictor</h2>
              <p className="text-gray-600 mt-2">Sign in or create an account to continue</p>
            </div>

            <div className="space-y-4">
              <Input
                type="email"
                placeholder="Email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
              <Input
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
              <Button className="w-full" onClick={() => handleAuth("login")}>
                Sign In
              </Button>
              <Button variant="outline" className="w-full" onClick={() => handleAuth("signup")}>
                Create Account
              </Button>
            </div>
          </div>
        </div>
      ) : (
        <div className="p-4">
          <nav className="bg-white shadow-sm mb-8 p-4">
            <div className="max-w-7xl mx-auto flex justify-between items-center">
              <h1 className="text-xl font-bold text-gray-800">HomePrice Predictor</h1>
              <Button variant="ghost" onClick={handleLogout}>
                Logout
              </Button>
            </div>
          </nav>

          <div className="max-w-2xl mx-auto bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-2xl font-bold text-gray-800 mb-6">Enter Property Details</h2>
            
            <div className="space-y-4">
              <div>
                <label className="block text-gray-700 mb-2">House Size (sq ft)</label>
                <Input
                  type="number"
                  value={formData.houseSize}
                  onChange={(e) => setFormData({ ...formData, houseSize: e.target.value })}
                />
              </div>

              <div>
                <label className="block text-gray-700 mb-2">Number of Bedrooms</label>
                <Input
                  type="number"
                  value={formData.bedrooms}
                  onChange={(e) => setFormData({ ...formData, bedrooms: e.target.value })}
                />
              </div>

              <div>
                <label className="block text-gray-700 mb-2">Location</label>
                <Input
                  value={formData.location}
                  onChange={(e) => setFormData({ ...formData, location: e.target.value })}
                />
              </div>

              <div>
                <label className="block text-gray-700 mb-2">Furnished State</label>
                <Select
                  value={formData.furnished}
                  onValueChange={(value) => setFormData({ ...formData, furnished: value })}
                >
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="fully">Fully Furnished</SelectItem>
                    <SelectItem value="semi">Semi Furnished</SelectItem>
                    <SelectItem value="unfurnished">Unfurnished</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <Button className="w-full" onClick={predictPrice}>
                Predict Price
              </Button>
            </div>

            {prediction && (
              <div className="mt-8 border-t pt-6">
                <h3 className="text-lg font-semibold text-gray-800 mb-4">Predicted Price Range</h3>
                <div className="text-3xl font-bold text-blue-500">{prediction}</div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
                      }
