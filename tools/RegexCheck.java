import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.util.regex.Pattern;
import java.util.regex.PatternSyntaxException;

public class RegexCheck {
    public static void main(String[] args) throws Exception {
        BufferedReader in = new BufferedReader(new InputStreamReader(System.in, StandardCharsets.UTF_8));
        int bad = 0;
        String line;
        while ((line = in.readLine()) != null) {
            if (line.isEmpty()) continue;
            try {
                Pattern.compile(line, Pattern.CASE_INSENSITIVE);
            } catch (PatternSyntaxException e) {
                System.out.println(line + ": " + e.getDescription());
                bad++;
            }
        }
        System.exit(bad == 0 ? 0 : 1);
    }
}
