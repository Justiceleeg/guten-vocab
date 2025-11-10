import { redirect } from "next/navigation";

export default function Home() {
  // Redirect to class overview page
  redirect("/class");
}
