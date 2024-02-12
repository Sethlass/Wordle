import java.io.*;
import java.net.*;
import java.util.*;
import java.util.stream.Collectors;

public class WordleServer {
    private static final int PORT = 1234; // Creates port
    private static final String[] WORDS = { // Word Bank
    "apple", "banjo", "crane", "dwarf", "eagle",
    "flame", "grape", "house", "ivory", "joker",
    "knife", "lemon", "mango", "nylon", "ocean",
    "piano", "quilt", "robot", "snake", "table",
    "ultra", "vocal", "watch", "xenon", "yacht",
    "zebra", "amber", "brave", "clown", "dance",
    "elbow", "fairy", "ghost", "honor", "ideal",
    "jolly", "kayak", "lunar", "magic", "novel",
    "olive", "pearl", "queen", "river", "sugar",
    "tiger", "unity", "value", "wheat", "xerox",
    "young", "stream", "actor", "bloom", "chalk",
    "chair", "breed", "cycle", "curve", "solve"
};
    private static String secretWord; // The word that needs to be guessed
    private static ServerSocket serverSocket; // Creates socket created by

    /**
     * The 'main' method is responsible for starting the server, allowing a client to connect to it,
     * and chooses a word that the client has to guess
     * @param args
     * @throws IOException
     */
    public static void main(String[] args) throws IOException {

        serverSocket = new ServerSocket(PORT); // Opens socket for client connection seth
        System.out.println("Server is listening on port " + PORT);

        try (Socket socket = serverSocket.accept(); // Indicates a connection was made
             PrintWriter out = new PrintWriter(socket.getOutputStream(), true); // Variable for output
             BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()))) { // Variable for input
            
            System.out.println("Client connected");
            selectRandomWord(); // Chooses word from the word bank
            String inputLine; // Gets client input lassiter

            while ((inputLine = in.readLine()) != null) { // While loop lasts until every character in the 'inputLine' is read
                String feedback = generateFeedback(inputLine.toLowerCase()); // Converts to lowercase for the print
                out.println(feedback);
            }
        } 
        catch (IOException e) { // Catches any errors that come from the client guess
            System.out.println("Exception caught when trying to listen on port " + PORT);
            System.out.println(e.getMessage());
        } 
        finally { // Closes server once the game has ended
            serverSocket.close();
        }
    }

    /*
    * Choses a random word from the word bank
    */
    private static void selectRandomWord() {
        Random rand = new Random();
        secretWord = WORDS[rand.nextInt(WORDS.length)];
    }

    /*
    * Builds a string based on the correctness of each letter in the client guess
    */
    private static String generateFeedback(String guess) {
        if (guess.length() != secretWord.length()) { // If the client guess is a different length than the secret word
            throw new IllegalArgumentException("Guess and secret word must be the same length.");
        }

        // Builds a string that will be sent to the client telling them the correctness of their guess
        StringBuilder feedback = new StringBuilder("XXXXX"); // Base feedback string
        Map<Character, Long> letterFrequency = secretWord.chars().boxed()
                .collect(Collectors.groupingBy(
                        k -> (char) k.intValue(),
                        Collectors.counting()
                ));
        
        // If the character 'i' in the client guess is in the correct spot, replace secretWord[i] with a 'G'
        for (int i = 0; i < secretWord.length(); i++) {
            if (guess.charAt(i) == secretWord.charAt(i)) {
                feedback.setCharAt(i, 'G');
                letterFrequency.put(guess.charAt(i), letterFrequency.get(guess.charAt(i)) - 1);
            }
        }

        // If character 'i' in the client guess is in the secretWord but not in the correct spot, then replace secretWord[i] with a 'Y'
        for (int i = 0; i < guess.length(); i++) {
            if (feedback.charAt(i) != 'G' && letterFrequency.getOrDefault(guess.charAt(i), 0L) > 0) {
                feedback.setCharAt(i, 'Y');
                letterFrequency.put(guess.charAt(i), letterFrequency.get(guess.charAt(i)) - 1);
            } 
            else if (feedback.charAt(i) != 'G') {
                feedback.setCharAt(i, 'X');
            }
        }

        return feedback.toString(); // Returns the modified feedback string
    }
}
